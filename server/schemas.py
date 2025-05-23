from pydantic import BaseModel
from datetime import datetime

class VideoOut(BaseModel):
    id: str
    title: str
    description: str | None = None
    published_at: datetime
    thumbnail_url: str

    class Config:
        "from_attributes" == True  
