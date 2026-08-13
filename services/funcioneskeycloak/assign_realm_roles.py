import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from services.funcioneskeycloak.get_realm_role import get_realm_role

async def assign_realm_roles(
    user_id: str,
    role_names: list[str]
):

    token = await get_admin_token()

    roles = []

    for role_name in role_names:

        role = await get_realm_role(role_name)

        roles.append({
            "id": role["id"],
            "name": role["name"]
        })

    url = (
        f"{get_admin_base_url()}"
        f"/users/{user_id}"
        "/role-mappings/realm"
    )

    async with httpx.AsyncClient() as client:

        response = await client.post(
            url,
            json=roles,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        response.raise_for_status()