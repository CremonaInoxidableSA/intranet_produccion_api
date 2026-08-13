import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from services.funcioneskeycloak.get_realm_role import get_realm_role

async def create_realm_role(role_name: str, description: str = ""):
    """
    Crea un rol en Keycloak.
    """

    token = await get_admin_token()

    url = (
        f"{get_admin_base_url()}"
        "/roles"
    )

    body = {
        "name": role_name,
        "description": description
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()

    role = await get_realm_role(role_name)
    
    return role