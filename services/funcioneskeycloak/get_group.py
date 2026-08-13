import httpx
import json

from core.config import settings
from services.funcioneskeycloak.get_admin_token import get_admin_token
from services.funcioneskeycloak.get_admin_base_url import get_admin_base_url

async def get_group(group_name: str):
    """
    Obtiene un grupo de Keycloak por nombre.
    """
    
    token = await get_admin_token()
    
    url = (
        f"{get_admin_base_url()}"
        "/groups"
    )
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        
        response.raise_for_status()
    
    groups = response.json()
    
    for group in groups:
        if group["name"] == group_name:
            return group
    
    raise Exception(f"El grupo '{group_name}' no existe.")