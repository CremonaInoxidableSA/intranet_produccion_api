from typing import Any

import httpx

from security.discovery import discovery


class JWKSClient:
    """
    Gestiona el conjunto de claves públicas (JWKS) publicadas
    por el proveedor OpenID Connect.

    Las claves se descargan una única vez y se mantienen en memoria
    para evitar realizar una petición HTTP en cada request de la API.
    """

    def __init__(self) -> None:
        self._jwks: dict[str, Any] | None = None

    async def load(self) -> dict[str, Any]:
        """
        Devuelve el JWKS cacheado.

        Si todavía no fue descargado, lo obtiene desde el proveedor
        OpenID Connect y lo almacena en memoria.
        """

        if self._jwks is not None:
            return self._jwks

        configuration = await discovery.load()

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(configuration["jwks_uri"])
            response.raise_for_status()

        jwks = response.json()

        if "keys" not in jwks:
            raise ValueError("El JWKS recibido no contiene la propiedad 'keys'.")

        self._jwks = jwks

        return self._jwks

    async def refresh(self) -> dict[str, Any]:
        """
        Fuerza una nueva descarga del JWKS.
        """

        self._jwks = None
        return await self.load()

    async def get_key(self, kid: str) -> dict[str, Any]:
        """
        Devuelve la clave pública correspondiente al 'kid'
        indicado en el JWT.

        Solo considera claves de firma RSA (RS256).
        """

        jwks = await self.load()

        key = self._find_key(jwks, kid)

        if key is not None:
            return key

        #
        # Es posible que Keycloak haya rotado las claves.
        # Intentamos descargarlas nuevamente una única vez.
        #

        jwks = await self.refresh()

        key = self._find_key(jwks, kid)

        if key is not None:
            return key

        raise ValueError(
            f"No se encontró una clave pública para el kid '{kid}'."
        )

    @staticmethod
    def _find_key(
        jwks: dict[str, Any],
        kid: str,
    ) -> dict[str, Any] | None:
        """
        Busca una clave pública válida para verificar
        un Access Token.

        Se aceptan únicamente claves:

        - use = sig
        - alg = RS256
        """

        for key in jwks["keys"]:

            if key.get("use") != "sig":
                continue

            if key.get("alg") != "RS256":
                continue

            if key.get("kid") == kid:
                return key

        return None


jwks_client = JWKSClient()