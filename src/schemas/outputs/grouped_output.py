from typing import List

from pydantic import BaseModel

from schemas.user_story_schema import UserStory


class GroupedOutput(BaseModel):
    users_stories:  List[UserStory]
    message: str

    class Config:
        orm_mode = True
        exclude_none = True
