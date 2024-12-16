from typing import Dict, List

from pydantic import BaseModel


class TestOutput(BaseModel):
    tests: List[Dict[str, str]]
    message: str

    class Config:
        orm_mode = True
        exclude_none = True
