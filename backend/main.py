from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from routes import donations

app = FastAPI()

# CORS - cross origin resource sharing - added coz my frontend and backend running two different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(donations.router)


#port running - http://127.0.0.1:5500/register.html