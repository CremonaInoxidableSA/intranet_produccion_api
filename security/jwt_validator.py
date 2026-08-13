from typing import Any

from jose import jwt
from jose.exceptions import JWTError

from core.config import settings
from schemas.authenticated_user import AuthenticatedUser
from security.jwt_decoder import decoder


class JWTValidator:
    """
    Valida JWT emitidos por Keycloak.

    Responsabilidades:

    - Validar firma.
    - Validar issuer.
    - Validar algoritmo.
    - Validar expiración.
    - Convertir el payload en AuthenticatedUser.
    """

    async def validate(
        self,
        token: str
    ) -> AuthenticatedUser:

        decoded = await decoder.decode(token)

        public_key = decoded["public_key"]

        try:

            payload: dict[str, Any] = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer=self.expected_issuer(),
                options={
                    "verify_aud": False
                }
            )

        except JWTError as error:

            raise ValueError(
                f"JWT inválido: {str(error)}"
            )

        return self.build_user(payload)

    def expected_issuer(self) -> str:
        """
        Construye el issuer esperado por Keycloak.
        """

        return (
            f"{settings.KEYCLOAK_URL}"
            f"/realms/{settings.KEYCLOAK_REALM}"
        )

    @staticmethod
    def build_user(
        payload: dict[str, Any]
    ) -> AuthenticatedUser:
        """
        Convierte los claims del JWT en nuestro modelo interno.
        """

        realm_access = payload.get(
            "realm_access",
            {}
        )

        roles = realm_access.get(
            "roles",
            []
        )

        groups = payload.get(
            "groups",
            []
        )

        return AuthenticatedUser(
            id=payload.get("sub"),

            username=payload.get(
                "preferred_username"
            ),

            email=payload.get(
                "email"
            ),

            first_name=payload.get(
                "given_name"
            ),

            last_name=payload.get(
                "family_name"
            ),

            roles=roles,

            groups=groups,

            raw_token=payload
        )


validator = JWTValidator()