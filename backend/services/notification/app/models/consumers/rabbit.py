from pydantic import Field
from typing import Optional
from .base import BaseConsumerSettings

class RabbitConsumerSettings(BaseConsumerSettings):
    """
    Strong-typed settings for RabbitMQ consumer.
    """

    host: str = Field(...)
    port: int = 5672
    username: Optional[str] = None
    password: Optional[str] = None
    queue_name: str = "events"
