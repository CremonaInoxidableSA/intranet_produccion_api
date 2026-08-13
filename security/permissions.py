from fastapi import Depends, HTTPException, status

from schemas.authenticated_user import AuthenticatedUser
from security.dependencies import get_current_user


def require_role(role: str):

    def dependency(
        usuario: AuthenticatedUser = Depends(get_current_user)
    ):

        # Buscar en roles directos del usuario
        tiene_rol_directo = role in usuario.roles
        
        # Buscar en grupos del usuario
        tiene_rol_en_grupo = role in usuario.groups

        if not (tiene_rol_directo or tiene_rol_en_grupo):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere el permiso '{role}'."
            )

        return usuario

    return dependency