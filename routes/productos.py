from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.productos import Productos
from models.productos_sectores import ProductosSectores

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/lista-productos")
def get_productos_total(id_sector: int):
    """Obtiene el listado de productos filtrado por `id_sector`. Requiere `id_sector` entero."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Productos)
            .join(ProductosSectores, Productos.id_producto == ProductosSectores.id_producto)
            .filter(ProductosSectores.id_sector == id_sector)
            .all()
        )
        result = [{
            "id_producto": 0,
            "nombre": "Otro"
        }] + [
            {
                "id_producto": p.id_producto,
                "nombre": p.nombre
            }
            for p in rows
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()