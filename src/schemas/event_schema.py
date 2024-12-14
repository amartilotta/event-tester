
from typing import Optional

from pydantic import BaseModel, Field


class Properties(BaseModel):
    distinct_id: str
    session_id: str
    journey_id: str
    current_url: str = Field(alias="$current_url")
    host: str = Field(alias="$host")
    pathname: str = Field(alias="$pathname")
    browser: str = Field(alias="$browser")
    device: str = Field(alias="$device")
    referrer: str = Field(alias="$referrer")
    referring_domain: str = Field(alias="$referring_domain")
    screen_height: int = Field(alias="$screen_height")
    screen_width: int = Field(alias="$screen_width")
    eventType: str
    elementType: str
    elementText: str
    elementAttributes: dict | None = Field(default=None)
    timestamp: str
    x: int
    y: int
    mouseButton: int
    ctrlKey: bool
    shiftKey: bool
    altKey: bool
    metaKey: bool

    class Config:
        allow_population_by_field_name = True


class EventSchema(BaseModel):
    event: str
    properties: Properties
    timestamp: str


    class Config:
        allow_population_by_field_name = True

