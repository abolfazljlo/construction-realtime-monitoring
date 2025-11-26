import asyncio
from pydantic import ConfigDict
from ..base import ForbidExtraModel

class BaseConsumerSettings(ForbidExtraModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )
    
    loop: asyncio.AbstractEventLoop

    