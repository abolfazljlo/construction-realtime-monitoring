from ...models.base import ForbidExtraModel
from ...models.consumers.rabbit import RabbitConsumerSettings

class RabbitMQConfig(ForbidExtraModel):
    enabled: bool = False
    host: str = "rabbit"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"
    queue_name: str = "notifications"

    def to_settings(self, loop):
        return RabbitConsumerSettings(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            queue_name=self.queue_name,
            loop=loop
        )