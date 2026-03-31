from pydantic import BaseModel

class Donation(BaseModel):
    donor_name: str
    food_type: str
    quantity: int
    location: str
    prepared_at: str  # or datetime if you handle conversion


class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str