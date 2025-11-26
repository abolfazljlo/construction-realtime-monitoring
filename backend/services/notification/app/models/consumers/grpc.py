from .base import BaseConsumerSettings

class GrpcConsumerSettings(BaseConsumerSettings):
    host: str = "0.0.0.0"
    port: int = 50052
