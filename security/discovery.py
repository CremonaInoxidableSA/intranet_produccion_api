import httpx

from core.config import settings


class OIDCDiscovery:
    """
    Descubre automáticamente la configuración OpenID Connect del proveedor
    de identidad (Keycloak en nuestro caso).

    La configuración se cachea en memoria para evitar una petición HTTP
    en cada request de la API.
    """

    def __init__(self):
        self._configuration = None

        self.discovery_url = (
            f"{settings.KEYCLOAK_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}"
            f"/.well-known/openid-configuration"
        )

    async def load(self) -> dict:
        """
        Devuelve la configuración OIDC.
        Si ya fue descargada anteriormente, la obtiene desde memoria.
        """

        if self._configuration is not None:
            return self._configuration

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.discovery_url)
            response.raise_for_status()

        self._configuration = response.json()

        return self._configuration

    async def refresh(self) -> dict:
        """
        Fuerza la descarga nuevamente del documento OIDC.
        """

        self._configuration = None
        return await self.load()


discovery = OIDCDiscovery()