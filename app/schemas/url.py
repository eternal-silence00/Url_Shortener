from pydantic import BaseModel, HttpUrl

class UrlCreate(BaseModel):
    url: HttpUrl
    
class UrlResponse(BaseModel):
    short_url: str
    
    class Config:
        from_attributes = True