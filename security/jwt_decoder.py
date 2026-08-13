from typing import Any

from jose import jwt

from security.jwks import jwks_client


class JWTDecoder:
    """
    Se encarga de preparar un JWT para su validación.

    No verifica la firma.

    Su única responsabilidad es:

    - Leer el Header.
    - Obtener el kid.
    - Buscar la clave pública correspondiente.
    """

    async def decode(self, token: str) -> dict[str, Any]:

        #
        # Leemos el Header SIN validar el JWT.
        #

        header = jwt.get_unverified_header(token)

        kid = header.get("kid")

        if kid is None:
            raise ValueError(
                "El JWT no contiene el campo 'kid'."
            )

        public_key = await jwks_client.get_key(kid)

        return {
            "header": header,
            "public_key": public_key
        }


decoder = JWTDecoder()