import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url

async def get_user(user_id: str):

    token = await get_admin_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    user_url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
    )

    roles_url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}/role-mappings/realm"
    )

    async with httpx.AsyncClient() as client:

        user_response = await client.get(
            user_url,
            headers=headers
        )

        user_response.raise_for_status()

        roles_response = await client.get(
            roles_url,
            headers=headers
        )

        roles_response.raise_for_status()

    user = user_response.json()

    user["realm_roles"] = [
        role["name"]
        for role in roles_response.json()
    ]

    return user