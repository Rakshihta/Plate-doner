from database import donations_collection, users_collection
from utils.security import hash_password, verify_password

# ---------------- DONATIONS ----------------
def add_donation(donation):
    donation_dict = donation.dict()

    donation_dict.pop("_id", None)

    donation_dict["status"] = "Available"

    result = donations_collection.insert_one(donation_dict)

    return {"message": "Donation added", "id": str(result.inserted_id)}

def get_donations(email=None):
    donations = []

    query = {}
    if email:
        query = {"email": {"$ne": email}}

    for d in donations_collection.find(query):
        d["_id"] = str(d["_id"])
        donations.append(d)

    return donations


# ---------------- USERS ----------------
def create_user(user):
    existing = users_collection.find_one({"email": user.email})

    if existing:
        return {"message": "Email already exists"}

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)

    users_collection.insert_one(user_dict)
    return {"message": "User created successfully"}


def authenticate_user(user):
    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        return None

    if not verify_password(user.password, db_user["password"]):
        return None

    return db_user