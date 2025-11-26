import os
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from .dispatcher.registry import create_handler_registry
from .dispatcher.dispatcher import NotificationDispatcher

from .consumer.rabbit_consumer import RabbitConsumer
from .consumer.grpc_consumer import GrpcConsumer

from .config.loader import load_service_config
from .utils.log import Log

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    # Try loading from project root
    root_env = Path(__file__).resolve().parent.parent.parent.parent.parent / ".env"
    if root_env.exists():
        load_dotenv(root_env)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Log.info("🚀 [NotificationService] Starting...")

    # -------------------------------
    # Load configuration
    # -------------------------------
    config = load_service_config()

    loop = asyncio.get_event_loop()
    dispatcher = NotificationDispatcher()

    # -------------------------------
    # Initialize handlers dynamically
    # -------------------------------
    handler_registry = create_handler_registry(config)
    dispatcher.bind_handler_registry(handler_registry)


    # -------------------------------
    # Initialize Consumers (conditional)
    # -------------------------------
    consumers = []

    # GRPC CONSUMER
    if config.consumers.grpc.enabled:
        grpc_settings = config.consumers.grpc
        grpc_consumer = GrpcConsumer(
            settings=grpc_settings.to_settings(loop),
            callback=dispatcher.dispatch
        )
        consumers.append(grpc_consumer)
        Log.info("🟢 gRPC consumer enabled")

    # RABBITMQ CONSUMER
    if config.consumers.rabbitmq.enabled:
        rabbit_settings = config.consumers.rabbitmq
        rabbit_consumer = RabbitConsumer(
            settings=rabbit_settings.to_settings(loop),
            callback=dispatcher.dispatch
        )
        consumers.append(rabbit_consumer)
        Log.info("🟢 RabbitMQ consumer enabled")

    if not consumers:
        Log.error("❌ No consumer enabled in configuration!")
        raise RuntimeError("At least one consumer must be enabled.")

    # -------------------------------
    # Start consumers safely
    # -------------------------------
    tasks = [asyncio.create_task(c.start(), name=c.__class__.__name__) for c in consumers]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)

    # Check for startup failures
    for task in done:
        exc = task.exception()
        if exc:
            Log.error(f"❌ Startup failure in {task.get_name()}: {exc}")

            for p in pending:
                p.cancel()
                try:
                    await p
                except asyncio.CancelledError:
                    pass

            # Graceful shutdown before exiting
            for c in consumers:
                await c.close()

            raise RuntimeError(f"Notification service failed on startup: {exc}") from exc

    Log.success("✅ Consumers started successfully")

    # Attach running consumers

    yield

    # -------------------------------
    # Shutdown Phase
    # -------------------------------
    Log.info("🛑 [NotificationService] Shutting down...")

    await asyncio.gather(*[c.close() for c in consumers])

    Log.success("👋 Notification service shutdown complete.")


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------

app = FastAPI(
    title="Notification Service",
    description="Handles SMS & Email notifications with dynamic providers",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", tags=["health"])
async def health():
    return {
        "status": "ok",
        "service": "notification",
    }
