import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from services.funcioneskeycloak.get_realm_role import get_realm_role

async def update_realm_role(old_role_name: str, new_role_name: str, description: str = ""):
    """
    Actualiza un rol en Keycloak (principalmente el nombre).
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/roles/{old_role_name}"
    )
    
    body = {
        "name": new_role_name,
        "description": description
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.put(
            url,
            json=body,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    role = await get_realm_role(new_role_name)
    
    return role