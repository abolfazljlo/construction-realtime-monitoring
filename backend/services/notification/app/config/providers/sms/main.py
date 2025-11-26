from .kavenegar import KavenegarSMSConfig
from .ghasedak import GhasedakSMSConfig
from .twilio import TwilioSMSConfig
from ....models.base import ForbidExtraModel

class SMSProvidersConfig(ForbidExtraModel):
    enabled: bool = True
    kavenegar: KavenegarSMSConfig
    ghasedak: GhasedakSMSConfig
    twilio: TwilioSMSConfig