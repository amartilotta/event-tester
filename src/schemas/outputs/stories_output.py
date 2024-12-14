from typing import List

from pydantic import BaseModel


class StoriesOutput(BaseModel):
    users_events:  List[dict]
