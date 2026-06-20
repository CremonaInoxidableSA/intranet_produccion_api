from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.labores import Labores

router = APIRouter(prefix="/labores", tags=["labores"])

@router.get("/lista-labores")
def get_labores_total(id_sector: int, id_producto: int):
    """Obtiene el listado de labores filtrado por `id_sector` e `id_producto`."""
    db = SessionLocal()
    try:
        rows = db.query(Labores).filter(
            Labores.id_sector == id_sector,
            Labores.id_producto == id_producto,
        ).all()
        return [
            {
                "id_labor": l.id_labor,
                "nombre": l.nombre
            }
            for l in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()