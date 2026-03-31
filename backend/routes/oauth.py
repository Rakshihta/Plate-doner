from fastapi import APIRouter, Request
from authlib.integrations.starlette_client import OAuth
from utils.jwt import create_access_token
import os

router = APIRouter(prefix="/auth", tags=["OAuth"])

oauth = OAuth()

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    jwt_token = create_access_token({"sub": user_info["email"]})

    return {
        "message": "Login successful",
        "user": user_info["email"],
        "access_token": jwt_token
    }

