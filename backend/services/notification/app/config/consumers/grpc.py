from ...models.base import ForbidExtraModel
from ...models.consumers.grpc import GrpcConsumerSettings

class GRPCConfig(ForbidExtraModel):
    enabled: bool = True
    host: str = "0.0.0.0"
    port: int = 50052

    def to_settings(self, loop):
        return GrpcConsumerSettings(
            host=self.host,
            port=self.port,
            loop=loop
        )