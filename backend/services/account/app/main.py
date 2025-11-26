import os
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from .resources.database import DatabaseResource
from .resources.redis import RedisResource
from .resources.jwt import JWTResource
from .resources.api_ir import ApiIrResource
from .services.identity_validator.api_ir import ApiIrIdentityValidator

from .api.v1.signup import signup_router

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
    Log.info("🚀 Starting...")

    # -------------------------------
    # Load configuration
    # -------------------------------
    config = load_service_config()

    # -------------------------------
    # Define Resources
    # -------------------------------
    db_resource = DatabaseResource(
        config.database
    )
    redis_resource = RedisResource(
        config.redis
    )
    jwt_resource = JWTResource(
        config.jwt
    )
    api_ir_resource = ApiIrResource(
        config.api_ir
    )

    resources = (
        db_resource,
        redis_resource,
        jwt_resource,
        api_ir_resource
    )

    # Attach running resources to the app state
    app.state.db = db_resource
    app.state.redis = redis_resource
    app.state.jwt = jwt_resource
    app.state.api_ir = api_ir_resource
    app.state.identity_validator = ApiIrIdentityValidator(api_ir_resource)

    # -------------------------------
    # Initailize consumers safely
    # -------------------------------
    tasks = [asyncio.create_task(r.initialize(), name=r.__class__.__name__) for r in resources]

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
            for r in resources:
                await r.close()

            raise RuntimeError(f"Account service failed on startup: {exc}") from exc

    Log.success("✅ Resources initialized successfully")

    yield

    # -------------------------------
    # Shutdown Phase
    # -------------------------------
    Log.info("🛑 Shutting down...")

    await asyncio.gather(*[r.close() for r in resources])

    Log.success("👋 Account service shutdown complete.")


# ---------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------

app = FastAPI(
    title="Account Service",
    description="",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health", tags=["health"])
async def health():
    return {
        "status": "ok",
        "service": "account",
    }

app.include_router(
    signup_router,
    prefix="/api/v1/signup"
)