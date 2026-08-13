from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from schemas.authenticated_user import AuthenticatedUser
from security.jwt_validator import validator


security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security_scheme
    )
) -> AuthenticatedUser:
    """
    Obtiene el usuario autenticado desde el JWT enviado
    en el header Authorization.

    Espera:

    Authorization: Bearer <token>
    """

    token = credentials.credentials

    try:

        user = await validator.validate(token)

        return user

    except Exception as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )