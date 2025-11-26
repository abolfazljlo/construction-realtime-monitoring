from abc import abstractmethod, ABC
from typing import Generic, TypeVar, Callable, Awaitable
from ..models.consumers.base import BaseConsumerSettings
from ..models.notification_message.union import NotificationMessage

T = TypeVar("T", bound=BaseConsumerSettings)

class BaseConsumer(ABC, Generic[T]):
    """
    Abstract base class for all notification consumers.
    Implements async lifecycle methods and uses strongly-typed settings.
    """

    def __init__(self, settings: T, callback: Callable[[NotificationMessage], Awaitable[None]]):
        super().__init__()

        self.__settings = settings
        self.__loop = self.__settings.loop

        self.__callbcak = callback

    @property
    def callback(self):
        return self.__callbcak

    @property
    def loop(self):
        """Expose strong-typed loop (read-only)"""
        return self.__loop

    @property
    def settings(self):
        """Expose strong-typed settings (read-only)"""
        return self.__settings

    @abstractmethod
    async def start(self):
        """Start consuming messages"""

    @abstractmethod
    async def close(self):
        """Gracefully stop consumer"""
    
