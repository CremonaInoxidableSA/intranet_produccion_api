import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url

async def get_group_roles(group_id: str):
    """
    Obtiene los realm_roles asignados a un grupo.
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}/role-mappings/realm"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    roles = response.json()
    
    return [role["name"] for role in roles]