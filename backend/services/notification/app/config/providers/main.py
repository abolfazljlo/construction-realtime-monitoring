from .email.main import EmailProvidersConfig
from .sms.main import SMSProvidersConfig
from ...models.base import ForbidExtraModel

class ProvidersConfig(ForbidExtraModel):
    sms: SMSProvidersConfig
    email: EmailProvidersConfig