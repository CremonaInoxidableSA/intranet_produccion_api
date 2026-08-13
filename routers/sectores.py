from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.db import SessionLocal
from models.sectores import Sectores

from security.permissions import require_role

router = APIRouter(
    prefix="/sectores", 
    tags=["sectores"]
)

@router.get(
    "/lista-sectores",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_SECTORES_PRODUCCION"))]
)
def get_sectores_total():
    """Obtiene el listado de todos los sectores, sin importar si están habilitados o no."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Sectores).all()
        )
        return [
            {
                "id_sector": s.id_sector,
                "nombre": s.nombre
            }
            for s in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()