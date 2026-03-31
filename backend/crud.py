import schemas
from database import donations_collection, users_collection
from utils.security import hash_password, verify_password


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


#authentication 
def create_user(user):
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    users_collection.insert_one(user_dict)
    return {"message": "User created"}

def authenticate_user(user):
    db_user = users_collection.find_one({"username": user.username})
    
    if not db_user:
        return None
    
    if not verify_password(user.password, db_user["password"]):
        return None
    
    return db_user