from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.labores import Labores
from models.sectores import Sectores

router = APIRouter(prefix="/labores", tags=["labores"])

@router.get("/lista-labores")
def get_labores_total(id_sector: int, id_producto: int):
    """Obtiene el listado de labores filtrado por `id_sector` e `id_producto`."""
    db = SessionLocal()
    try:
        rows = db.query(Labores).filter(
            Labores.id_sector == id_sector,
            Labores.id_producto == id_producto,
            Labores.habilitado == True
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

@router.get("/lista-labores-general")
def get_labores_general(id_producto: int):
    """Obtiene el listado de labores filtrado por `id_producto`"""
    db = SessionLocal()
    try:
        rows = db.query(Labores, Sectores).join(
            Sectores, Labores.id_sector == Sectores.id_sector
        ).filter(
            Labores.id_producto == id_producto
        ).all()
        return [
            {
                "id_labor": l.id_labor,
                "nombre": l.nombre,
                "habilitado": l.habilitado,
                "sector": s.nombre
            }
            for l, s in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()