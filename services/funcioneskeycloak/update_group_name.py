import httpx
import json

from core.config import settings

from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url

async def update_group_name(group_id: str, new_name: str):
    """
    Actualiza el nombre de un grupo.
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}"
    )
    
    body = {
        "name": new_name
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
    
    group_url = (
        f"{get_admin_base_url()}"
        f"/groups/{group_id}"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            group_url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    return response.json()