from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import httpx
from os import getenv
from secrets import token_urlsafe
from typing import Optional

load_dotenv()

# Discord OAuth2 configuration
DISCORD_CLIENT_ID = getenv("DISCORD_APP_CLIENT_ID")
DISCORD_CLIENT_SECRET = getenv("DISCORD_APP_SECRET")
REDIRECT_URI = getenv("REDIRECT_URI")
DISCORD_AUTH_URL = "https://discord.com/api/oauth2/authorize"
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_URL = "https://discord.com/api/users/@me"

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=getenv("SECRET_KEY"))

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

@app.get("/")
async def index(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"user": user, "error": None}
    )

@app.get("/authenticate")
async def authenticate(request: Request):
    state = token_urlsafe(16)
    request.session["state"] = state
    auth_url = (
        f"{DISCORD_AUTH_URL}?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code"
        f"&scope=identify&state={state}"
    )
    return RedirectResponse(auth_url)

@app.get("/oauth2")
async def oauth2(request: Request, code: Optional[str] = None, state: Optional[str] = None):
    if state != request.session.get("state"):
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")

    try:
        async with httpx.AsyncClient() as client:
            # Exchange code for access token
            token_response = await client.post(
                DISCORD_TOKEN_URL,
                data={
                    "client_id": DISCORD_CLIENT_ID,
                    "client_secret": DISCORD_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )

            if token_response.status_code != 200:
                raise HTTPException(status_code=403, detail="Invalid or expired code")

            token_data = token_response.json()
            access_token = token_data.get("access_token")

            # Fetch user data
            user_response = await client.get(
                DISCORD_API_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if user_response.status_code != 200:
                raise HTTPException(status_code=403, detail="Failed to fetch user data")

            user_data = user_response.json()
            request.session["user"] = user_data

    except httpx.HTTPStatusError as e:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"user": None, "error": f"Authentication failed: {str(e)}"}
        )

    return RedirectResponse(url="/")

@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")