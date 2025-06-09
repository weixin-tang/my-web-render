from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
from crud import get_web_page_by_id, get_all_web_pages

router = APIRouter( prefix="/web-render" , tags=["Pages"] )
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """首页 - 显示上传表单和网页列表"""
    pages = get_all_web_pages(db, limit=10)
    return templates.TemplateResponse(
        "upload.html", 
        {"request": request, "pages": pages}
    )

@router.get("/view/{page_id}", response_class=HTMLResponse)
async def view_page(page_id: str, db: Session = Depends(get_db)):
    """显示网页内容"""
    db_page = get_web_page_by_id(db, page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="网页不存在")
    
    # 直接返回HTML内容
    return HTMLResponse(content=db_page.html_content)

@router.get("/preview/{page_id}", response_class=HTMLResponse)
async def preview_page(request: Request, page_id: str, db: Session = Depends(get_db)):
    """预览网页（在模板中显示）"""
    db_page = get_web_page_by_id(db, page_id)
    if not db_page:
        raise HTTPException(status_code=404, detail="网页不存在")
    
    return templates.TemplateResponse(
        "display.html",
        {
            "request": request,
            "page": db_page,
            "html_content": db_page.html_content
        }
    )

@router.get("/list", response_class=HTMLResponse)
async def list_pages(request: Request, db: Session = Depends(get_db)):
    """网页列表页面"""
    pages = get_all_web_pages(db)
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "pages": pages}
    )

