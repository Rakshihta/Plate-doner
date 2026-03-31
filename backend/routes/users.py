from fastapi import APIRouter, HTTPException
import schemas, crud
from utils.jwt import create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
def signup(user: schemas.UserCreate):
    return crud.create_user(user)

@router.post("/login")
def login(user: schemas.UserLogin):
    db_user = crud.authenticate_user(user)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user["username"]})
    return {"access_token": token}