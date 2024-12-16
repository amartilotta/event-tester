from typing import List

from pydantic import BaseModel

from schemas.user_story_schema import Pattern


class PatternsOutput(BaseModel):
    patterns: List[Pattern]
    message: str

    class Config:
        orm_mode = True
        exclude_none = True
