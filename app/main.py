import discordoauth2
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from os import getenv


load_dotenv()


DISCORD_APP_CLIENT_ID = getenv("DISCORD_APP_CLIENT_ID")
DISCORD_APP_SECRET = getenv("DISCORD_APP_SECRET")


client = discordoauth2.Client(
    DISCORD_APP_CLIENT_ID,
    secret=DISCORD_APP_SECRET,
    redirect="http://localhost:8080/oauth2",
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="./static/templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/authenticate")
async def main():
    return RedirectResponse(client.generate_uri(scope=["identify"]))


@app.get("/oauth2")
async def oauth2(request: Request):
    code = request.query_params.get("code")
    context = {"request": request, "user": None, "error": None}

    try:
        access = client.exchange_code(code)
        identify = access.fetch_identify()
        context["user"] = identify
    except discordoauth2.exceptions.Exceptions.HTTPException:
        context["error"] = "Authentication failed. Please try again."
        return HTTPException(status_code=403, detail="Access code is expired/invalid")

    return templates.TemplateResponse(
        request=request, name="index.html", context=context
    )
