import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url
from services.funcioneskeycloak.get_group import get_group

async def create_group(group_name: str):
    """
    Crea un grupo en Keycloak.
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        "/groups"
    )
    
    body = {
        "name": group_name
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
    
    group = await get_group(group_name)
    
    return group