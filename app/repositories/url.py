from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.url import Url

class UrlRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_url(self, url:str, short_code:str):
        url = Url(url=url, short_code=short_code)
        self.session.add(url)
        await self.session.flush()
        await self.session.refresh(url)
        return url
    
    async def get_by_short_code(self, short_code: str):
        result = await self.session.execute(select(Url).where(Url.short_code == short_code))
        return result.scalar_one_or_none()
    
    async def get_all(self, limit: int = 10, offset: int = 0):
        result = await self.session.execute(select(Url).limit(limit).offset(offset))
        return result.scalars().all()
    
    async def get_by_url(self, url:str):
        result = await self.session.execute(select(Url).where(Url.url == url))
        return result.scalar_one_or_none()