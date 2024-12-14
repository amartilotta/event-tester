from typing import List

from pydantic import BaseModel

from schemas.event_schema import EventSchema


class EventsInput(BaseModel):
    events: List[EventSchema]

    class Config:
        allow_population_by_field_name = True
