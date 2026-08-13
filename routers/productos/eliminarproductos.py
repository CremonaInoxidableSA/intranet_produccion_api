from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.productos import Productos

class EliminarProducto(BaseModel):
    id_producto: int

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/eliminar-producto")
def eliminar_producto(data: EliminarProducto):
    """Elimina un producto si existe."""
    db = SessionLocal()
    try:
        producto = db.query(Productos).filter(Productos.id_producto == data.id_producto).first()
        
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if producto.nombre == "Otro":
            return {
                "detail": "El producto 'Otro' no puede ser eliminado",
                "success": False
            }
        
        if producto.habilitado == False:
            return {
                "detail": "El producto ya está eliminado",
                "success": False
            }

        producto.habilitado = False
        db.commit()
        
        return {
            "detail": "Producto eliminado exitosamente",
            "success": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()