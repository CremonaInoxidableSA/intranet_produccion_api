from typing import Any

from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    """
    Usuario autenticado obtenido desde un JWT válido
    emitido por Keycloak.
    """

    id: str = Field(
        description="Identificador único del usuario en Keycloak (sub)"
    )

    username: str | None = Field(
        default=None,
        description="Nombre de usuario de Keycloak"
    )

    email: str | None = Field(
        default=None,
        description="Correo electrónico del usuario"
    )

    first_name: str | None = Field(
        default=None,
        description="Nombre del usuario"
    )

    last_name: str | None = Field(
        default=None,
        description="Apellido del usuario"
    )

    roles: list[str] = Field(
        default_factory=list,
        description="Roles asignados al usuario"
    )

    groups: list[str] = Field(
        default_factory=list,
        description="Grupos a los que pertenece el usuario"
    )

    raw_token: dict[str, Any] | None = Field(
        default=None,
        description="Payload original del JWT"
    )