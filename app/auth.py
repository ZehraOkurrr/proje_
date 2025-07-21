import os
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import httpx
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


@router.get("/login")
def login():
    redirect_uri = "http://localhost:8001/auth/callback"
    return RedirectResponse(
        f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={redirect_uri}&scope=read:user"
    )


@router.get("/callback")
async def auth_callback(code: str):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
        )
        token_json = token_res.json()
        access_token = token_json.get("access_token")

        # Kullanıcı bilgilerini çek
        user_res = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_res.json()

    return {
        "username": user_data["login"],
        "name": user_data.get("name"),
        "avatar": user_data.get("avatar_url"),
    }
