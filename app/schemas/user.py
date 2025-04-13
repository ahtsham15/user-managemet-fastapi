from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str
    firstName:str
    lastName:str
    
class UserLogin(BaseModel):
    email:str
    password:str
    
class UserUpdate(BaseModel):
    email:Optional[str]=None
    password:Optional[str]=None
    firstName:Optional[str]=None
    lastName:Optional[str]=None

class UserResponse(BaseModel):
    id: int
    email: str
    firstName: Optional[str] = None
    lastName: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)