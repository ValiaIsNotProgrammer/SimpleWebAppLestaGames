from pydantic import BaseModel
from typing import Optional

class File(BaseModel):
    filename: str
    contents: bytes

    class Config:
        schema_extra = {
            "example": {
                "filename": "example.txt",
                "contents": b"Hello World"
            }
        }
