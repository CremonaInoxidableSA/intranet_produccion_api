from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.productos import Productos
from models.labores import Labores
from sqlalchemy import func
import json

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/lista-productos")
def get_productos_total(id_sector: int):
    """Obtiene el listado de productos filtrado por `id_sector`. Requiere `id_sector` entero."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Productos).filter(func.JSON_CONTAINS(Productos.sectores, json.dumps(id_sector))).all()
        )
        return [
            {
                "id_producto": p.id_producto,
                "nombre": p.nombre
            }
            for p in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

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