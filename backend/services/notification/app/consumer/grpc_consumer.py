import json
import grpc
from typing import Callable, Awaitable, Optional

from .base import BaseConsumer
from ..models.consumers.grpc import GrpcConsumerSettings
from ..models.notification_message.union import NotificationMessage
from ..proto import notification_pb2_grpc, notification_pb2
from ..utils.log import Log

class GrpcConsumer(BaseConsumer[GrpcConsumerSettings]):
    """
    gRPC consumer that exposes a NotificationService
    allowing other services to push notifications.
    """

    def __init__(
        self,
        settings: GrpcConsumerSettings,
        callback: Callable[[NotificationMessage], Awaitable[None]]
    ) -> None:
        super().__init__(settings, callback)
        self.__server: Optional[grpc.aio.Server] = None

    async def start(self) -> None:
        """Start gRPC server and listen for incoming notifications."""

        self.__server = grpc.aio.server()

        # Register service
        notification_pb2_grpc.add_NotificationServiceServicer_to_server(
            self.NotificationServicer(self.callback),
            self.__server,
        )

        listen_addr: str = f"{self.settings.host}:{self.settings.port}"
        self.__server.add_insecure_port(listen_addr)

        Log.info(f"[GrpcConsumer] gRPC listening on {listen_addr}")

        await self.__server.start()

    async def close(self) -> None:
        """Gracefully shut down gRPC server."""
        if self.__server is not None:
            await self.__server.stop(0)
            Log.info("[GrpcConsumer] gRPC server stopped")

    # ------------------------------------------------------------------
    # Inner Servicer
    # ------------------------------------------------------------------
    class NotificationServicer(notification_pb2_grpc.NotificationServiceServicer):
        """
        This servicer gets called by gRPC when another service calls SendNotification().
        """

        def __init__(
            self,
            callback: Callable[[NotificationMessage], Awaitable[None]]
        ) -> None:
            self.__callback = callback

        async def SendNotification(
            self,
            request: notification_pb2.NotificationRequest,
            context: grpc.aio.ServicerContext
        ) -> notification_pb2.Ack:

            try:
                # Convert JSON → dict
                raw_dict = json.loads(request.payload_json)

                # Validate + cast dict → NotificationMessage
                notif_message: NotificationMessage = NotificationMessage.model_validate(raw_dict)

                # Call notification dispatcher / handler
                await self.__callback(notif_message)

                success = True
            except Exception as e:
                Log.info(f"[GrpcConsumer] Error processing gRPC notification: {e}")
                success = False

            return notification_pb2.Ack(success=success)