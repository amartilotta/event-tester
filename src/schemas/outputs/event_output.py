from typing import List

from pydantic import BaseModel


class EventsOutput(BaseModel):
    events: List[dict]
    message: str
