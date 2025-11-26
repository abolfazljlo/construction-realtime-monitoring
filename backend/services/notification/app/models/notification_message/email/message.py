from typing import Literal
from .data import EmailData
from ..message_base import BaseNotificationMessage
from ....enum.notification_type import NotificationType

class EmailNotificationMessage(BaseNotificationMessage):
    type: Literal[NotificationType.EMAIL]
    data: EmailData