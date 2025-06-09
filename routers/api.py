from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from database import get_db
from schemas import WebPageCreate, WebPageResponse, WebPageURL
from crud import create_web_page, get_web_page_by_id, get_all_web_pages, delete_web_page
from typing import List

router = APIRouter(prefix="/web-render/api", tags=["API"])

@router.post("/pages", response_model=WebPageURL, status_code=status.HTTP_201_CREATED)
async def create_page(page_data: WebPageCreate, db: Session = Depends(get_db)):
    """创建新网页并返回访问URL"""
    try:
        db_page = create_web_page(db, page_data)
        return WebPageURL(
            page_id=db_page.page_id,
            url=f"/view/{db_page.page_id}",
            message="网页创建成功"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建网页失败: {str(e)}"
        )

@router.get("/pages", response_model=List[WebPageResponse])
async def list_pages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取所有网页列表"""
    pages = get_all_web_pages(db, skip=skip, limit=limit)
    return pages

@router.get("/pages/{page_id}", response_model=WebPageResponse)
async def get_page(page_id: str, db: Session = Depends(get_db)):
    """获取特定网页信息"""
    db_page = get_web_page_by_id(db, page_id)
    if not db_page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="网页不存在"
        )
    return db_page

@router.delete("/pages/{page_id}")
async def delete_page(page_id: str, db: Session = Depends(get_db)):
    """删除网页"""
    success = delete_web_page(db, page_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="网页不存在"
        )
    return {"message": "网页删除成功"}

