from ...models.base import ForbidExtraModel
from .grpc import GRPCConfig
from .rabbit import RabbitMQConfig

class ConsumersConfig(ForbidExtraModel):
    grpc: GRPCConfig
    rabbitmq: RabbitMQConfig