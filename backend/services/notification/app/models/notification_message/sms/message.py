from typing import Literal
from .data import SMSData
from ..message_base import BaseNotificationMessage
from ....enum.notification_type import NotificationType

class SMSNotificationMessage(BaseNotificationMessage):
    type: Literal[NotificationType.SMS]
    data: SMSData
