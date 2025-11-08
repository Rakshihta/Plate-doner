from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import donations_collection
from bson import ObjectId

app = FastAPI()

# 🔥 Add this block
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Donation(BaseModel):
    donor_name: str
    food_type: str
    quantity: int
    location: str
    prepared_at: str  # or datetime if you handle conversion

@app.post("/donations")
def add_donation(donation: Donation):
    donation_dict = donation.dict()
    result = donations_collection.insert_one(donation_dict)
    return {"message": "Donation added successfully", "id": str(result.inserted_id)}

@app.get("/donations")
def get_donations():
    donations = []
    for donation in donations_collection.find():
        donation["_id"] = str(donation["_id"])
        donations.append(donation)
    return donations
