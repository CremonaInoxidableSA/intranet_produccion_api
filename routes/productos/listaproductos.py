from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.productos import Productos
from models.productos_sectores import ProductosSectores
from models.sectores import Sectores

class ActualizarProducto(BaseModel):
    id_producto: int
    nombre: str

router = APIRouter(prefix="/productos", tags=["productos"])

@router.get("/lista-productos-sector")
def get_productos_sector(id_sector: int):
    """Obtiene el listado de productos filtrado por `id_sector`. Requiere `id_sector` entero."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Productos)
            .join(ProductosSectores, Productos.id_producto == ProductosSectores.id_producto)
            .filter(ProductosSectores.id_sector == id_sector, Productos.habilitado == True)
            .all()
        )
        result = [
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

@router.get("/lista-productos-general")
def get_productos_total():
    """Obtiene el listado de productos sin filtros agregados, con sus sectores asociados"""
    db = SessionLocal()
    try:
        rows = (
            db.query(Productos, Sectores)
            .join(ProductosSectores, Productos.id_producto == ProductosSectores.id_producto)
            .join(Sectores, ProductosSectores.id_sector == Sectores.id_sector)
            .filter(Productos.habilitado == True)
            .all()
        )
        
        productos_dict = {}
        for producto, sector in rows:
            if producto.id_producto not in productos_dict:
                productos_dict[producto.id_producto] = {
                    "id_producto": producto.id_producto,
                    "nombre": producto.nombre,
                    "sectores": []
                }
            productos_dict[producto.id_producto]["sectores"].append(sector.nombre)
        
        result = list(productos_dict.values())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()