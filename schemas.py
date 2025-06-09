from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WebPageCreate(BaseModel):
    title: Optional[str] = None
    html_content: str

class WebPageResponse(BaseModel):
    id: int
    page_id: str
    title: Optional[str]
    html_content: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class WebPageURL(BaseModel):
    page_id: str
    url: str
    message: str