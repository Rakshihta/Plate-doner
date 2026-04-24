from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId
from routes import donations, users, oauth
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# CORS - cross origin resource sharing - added coz my frontend and backend running two different ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://incomparable-churros-ffa3a4.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Session - for OAuth
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

app.include_router(donations.router)
app.include_router(users.router)
app.include_router(oauth.router)


#port running - http://127.0.0.1:5500/register.html