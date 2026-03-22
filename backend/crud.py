import schemas
from database import donations_collection


def add_donation(donation: schemas.Donation):
    donation_dict = donation.dict()
    result = donations_collection.insert_one(donation_dict)
    return {"message": "Donation added successfully", "id": str(result.inserted_id)}

def get_donations():
    donations = []
    for donation in donations_collection.find():
        donation["_id"] = str(donation["_id"])
        donations.append(donation)
    return donations