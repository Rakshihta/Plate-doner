from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
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

# ---------- STEP 1: Redirect to Google ----------
@router.get("/login")
async def login(request: Request):
    redirect_uri = "https://your-backend.onrender.com/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


# ---------- STEP 2: Handle Google Callback ----------
@router.get("/callback")
async def auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    jwt_token = create_access_token({"sub": user_info["email"]})

    # ✅ Redirect to frontend with token
    return RedirectResponse(
    url=f"https://incomparable-churros-ffa3a4.netlify.app/login.html?token={jwt_token}",
    status_code=302
    )

