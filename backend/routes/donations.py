import schemas
import crud
from fastapi import APIRouter

router = APIRouter(prefix="/donations", tags=["Donations"])

@router.post("/")
def add(donation: schemas.Donation):
    return crud.add_donation(donation)

@router.get("/")
def get_don():
    return crud.get_donations()