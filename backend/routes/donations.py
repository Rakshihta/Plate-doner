import schemas
import crud
from fastapi import APIRouter

router = APIRouter(prefix="/donations", tags=["Donations"])


# ================= ADD DONATION =================
@router.post("/")
def add(donation: schemas.Donation):
    return crud.add_donation(donation)


# ================= GET DONATIONS =================
@router.get("/")
def get_don(email: str = None):
    return crud.get_donations(email)