from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.url import UrlRepository
from app.database import get_db
from app.schemas.url import UrlCreate, UrlResponse
from app.services.url import create_short_code
from fastapi.responses import RedirectResponse

router = APIRouter()

@router.post("/url",response_model=UrlResponse, status_code=201)
async def create_short_url(
    data: UrlCreate,
    session: AsyncSession = Depends(get_db)
):
    short_url = await create_short_code(data.url, session)
    return {"short_url": short_url}

@router.get("/url")
async def get_short_urls(
    limit: int = 10,
    offset: int = 0,
    session: AsyncSession = Depends(get_db)
):
    repo = UrlRepository(session)
    result = await repo.get_all(limit, offset)
    return result 
    
    
@router.get("/{short_code}")
async def redirect(
    short_code: str,
    session: AsyncSession = Depends(get_db)
):
    repo = UrlRepository(session)
    result = await repo.get_by_short_code(short_code)
    if not result:
        raise HTTPException(status_code=404, detail="Url not found")
    return RedirectResponse(url=result.url)