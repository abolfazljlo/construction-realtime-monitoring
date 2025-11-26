from .smtp import SMTPEmailConfig
from .sendgrid import SendGridEmailConfig
from ....models.base import ForbidExtraModel

class EmailProvidersConfig(ForbidExtraModel):
    enabled: bool = True
    smtp: SMTPEmailConfig
    sendgrid: SendGridEmailConfig