from typing import Dict, Type
from ..utils.log import Log
from ..models.notification_message.message_base import BaseNotificationMessage
from .handlers.base import HandlerInterface

class NotificationDispatcher:
    """
    Routes NotificationMessage instances to their appropriate handler.

    Handler registry example:
        {
            EmailNotificationMessage: EmailHandler(...),
            SMSNotificationMessage: SMSHandler(...),
        }
    """

    def __init__(self):
        self._registry: Dict[Type[BaseNotificationMessage], HandlerInterface] = {}

    # ---------------------------------------------------------
    # BIND REGISTRY (dynamic from config.yml)
    # ---------------------------------------------------------
    def bind_handler_registry(self, registry: Dict[Type, HandlerInterface]):
        """
        Binds a dynamic handler registry to the dispatcher.
        Overwrites any previous registry.
        """
        if not isinstance(registry, dict):
            raise TypeError("Registry must be a dictionary {MessageType: Handler}")

        # OPTIONAL: Validate handlers implement 'handle'
        for msg_type, handler in registry.items():
            if not hasattr(handler, "handle"):
                raise RuntimeError(
                    f"Handler for {msg_type.__name__} does not implement 'handle()'"
                )

        self._registry = registry
        Log.success("🔗 Handler registry successfully bound to dispatcher")

    # ---------------------------------------------------------
    # DISPATCH
    # ---------------------------------------------------------
    async def dispatch(self, message: BaseNotificationMessage):
        """
        Dispatch a single notification message to the correct handler.
        """

        msg_type = type(message)
        handler = self._registry.get(msg_type)

        if handler is None:
            Log.error(
                f"❌ No handler registered for message type: {msg_type.__name__}"
            )
            return

        try:
            await handler.handle(message)
        except Exception as e:
            Log.error(
                f"❌ Handler failure for {msg_type.__name__}: {e}"
            )
            raise
