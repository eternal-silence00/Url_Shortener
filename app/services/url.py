from app.repositories.url import UrlRepository
from fastapi import Depends, HTTPException
from app.config import settings
from app.database import get_db
import random
import string

alphabet = string.ascii_letters + string.digits

async def create_short_code(url: str, db = Depends(get_db)):
    max_attemps = 5
    current_attemps = 0
    repo = UrlRepository(db)
    old_short_code = await repo.get_by_url(url)
    if old_short_code:
        return f"{settings.base_url}/{old_short_code.short_code}"
    while current_attemps < max_attemps:
        short_code = "".join(random.choices(alphabet, k=8))
        old_url = await repo.get_by_short_code(short_code)
        if not old_url:
            await repo.create_url(url,short_code)
            return f"{settings.base_url}/{short_code}"
        current_attemps += 1
    raise HTTPException(status_code=400, detail="Failure")
    
    
