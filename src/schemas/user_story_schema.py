from typing import List, Optional

from pydantic import BaseModel

from schemas.event_schema import EventSchema


class Action(BaseModel):
    type: str
    class_: Optional[str] = None
    target: Optional[str] = None
    value: Optional[str] = None
    url: Optional[str] = None
    selector: Optional[str] = None

    class Config:
        orm_mode = True
        exclude_none = True

class UserStory(BaseModel):
    id: str
    title: str
    actions: List[Action]

    class Config:
        orm_mode = True
        exclude_none = True

class Pattern(BaseModel):
    pattern: str
    count: int

class StorySchema(BaseModel):
    session_id: str
    user_history: List[EventSchema]

    class Config:
        orm_mode = True
        exclude_none = True
