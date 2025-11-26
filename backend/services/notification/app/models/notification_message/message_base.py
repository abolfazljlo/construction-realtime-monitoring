from ..base import ForbidExtraModel
from ...enum.notification_type import NotificationType

class BaseNotificationMessage(ForbidExtraModel):
    type: NotificationType
