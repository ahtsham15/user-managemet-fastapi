from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    firstName:str
    lastName:str
    
class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id: int
    email: str
    firstName:str
    lastName:str

    class Config:
        orm_mode = True