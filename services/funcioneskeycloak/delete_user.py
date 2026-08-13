import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url

async def delete_user(user_id: str):

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.delete(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()