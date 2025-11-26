from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from pydantic import BaseModel

S = TypeVar("S", bound=BaseModel)
class ResourceInterface(ABC, Generic[S]):

    def __init__(self, settings: S):
        super().__init__()
        self.__settings = settings

    @property
    def settings(self):
        return self.__settings
    
    @abstractmethod
    async def initialize(self): ...

    @abstractmethod
    async def close(self): ...