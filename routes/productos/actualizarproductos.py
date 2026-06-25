from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.productos import Productos

class ActualizarProducto(BaseModel):
    id_producto: int
    nombre: str

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/actualizar-nombre-producto")
def actualizar_producto(data: ActualizarProducto):
    """Actualiza el nombre de un producto si es diferente al actual y no está vacío."""
    db = SessionLocal()
    try:
        producto = db.query(Productos).filter(Productos.id_producto == data.id_producto).first()
        
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if producto.nombre == "Otro":
            return {
                "detail": "El producto 'Otro' no puede ser modificado",
                "success": False
            }
        
        if data.nombre.strip() == "Otro":
            return {
                "detail": "'Otro' no puede ser asignado como nombre",
                "success": False
            }
        
        if data.nombre.strip() == "":
            return {
                "detail": "El nombre del producto no debe estar vacío",
                "success": False
            }
        
        if data.nombre.strip() == producto.nombre:
            return {
                "detail": "El nombre del producto debe ser diferente al actual",
                "success": False
            }

        producto.nombre = data.nombre
        db.commit()
        
        return {
            "detail": "Producto actualizado exitosamente",
            "success": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()