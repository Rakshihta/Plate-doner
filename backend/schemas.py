from pydantic import BaseModel, EmailStr

class Donation(BaseModel):
    donor_name: str
    email: EmailStr   
    food_type: str
    quantity: int
    location: str
    prepared_at: str
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str