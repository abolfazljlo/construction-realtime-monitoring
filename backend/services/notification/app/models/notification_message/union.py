from typing import Annotated, Union
from pydantic import Field

from .email.message import EmailNotificationMessage
from .sms.message import SMSNotificationMessage

NotificationMessage = Annotated[
    Union[EmailNotificationMessage, SMSNotificationMessage],
    Field(discriminator="type")
]
