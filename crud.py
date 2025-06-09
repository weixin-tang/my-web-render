from sqlalchemy.orm import Session
from models import WebPage
from schemas import WebPageCreate
import uuid
import re

def generate_page_id() -> str:
    """生成唯一的页面ID"""
    return str(uuid.uuid4())[:8]

def extract_title_from_html(html_content: str) -> str:
    """从HTML中提取标题"""
    title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    return "Untitled Page"

def create_web_page(db: Session, page_data: WebPageCreate) -> WebPage:
    """创建新的网页记录"""
    page_id = generate_page_id()
    
    # 如果没有提供标题，尝试从HTML中提取
    title = page_data.title
    if not title:
        title = extract_title_from_html(page_data.html_content)
    
    db_page = WebPage(
        page_id=page_id,
        title=title,
        html_content=page_data.html_content
    )
    
    db.add(db_page)
    db.commit()
    db.refresh(db_page)
    return db_page

def get_web_page_by_id(db: Session, page_id: str) -> WebPage:
    """根据页面ID获取网页"""
    return db.query(WebPage).filter(WebPage.page_id == page_id).first()

def get_all_web_pages(db: Session, skip: int = 0, limit: int = 100):
    """获取所有网页列表"""
    return db.query(WebPage).offset(skip).limit(limit).all()

def delete_web_page(db: Session, page_id: str) -> bool:
    """删除网页"""
    db_page = get_web_page_by_id(db, page_id)
    if db_page:
        db.delete(db_page)
        db.commit()
        return True
    return False