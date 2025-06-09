from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class WebPage(Base):
    __tablename__ = "web_pages"
    
    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=True)
    html_content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<WebPage(page_id='{self.page_id}', title='{self.title}')>"