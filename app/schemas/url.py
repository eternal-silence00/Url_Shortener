from pydantic import BaseModel

class UrlCreate(BaseModel):
    url: str
    
class UrlResponse(BaseModel):
    short_url: str
    
    class Config:
        from_attributes = True