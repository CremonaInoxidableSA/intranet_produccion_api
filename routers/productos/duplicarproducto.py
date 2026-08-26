from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import func
from config.db import SessionLocal
from models.productos import Productos
from models.productos_sectores import ProductosSectores
from models.labores import Labores

from security.permissions import require_role

class DuplicarProductoRequest(BaseModel):
    id_producto: int

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post(
    "/duplicar-producto",
    dependencies=[Depends(require_role("PERMISO_CREAR_PRODUCTOS_PRODUCCION"))]
)
def duplicar_producto(data: DuplicarProductoRequest):
    """
    Duplica un producto existente, copiando sus asociaciones con sectores y labores.
    
    Parámetros:
    - id_producto: id del producto a duplicar
    """
    db = SessionLocal()
    try:
        # Buscar el producto original por id
        producto_original = db.query(Productos).filter(
            Productos.id_producto == data.id_producto
        ).first()
        
        if not producto_original:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró un producto con el id {data.id_producto}"
            )
        
        nombre_copia_base = f"{producto_original.nombre} - copia"
        nombre_copia = nombre_copia_base
        contador = 1
        
        while True:
            existe = db.query(Productos).filter(
                func.lower(Productos.nombre) == func.lower(nombre_copia)
            ).first()
            
            if not existe:
                break
            
            nombre_copia = f"{nombre_copia_base} {contador}"
            contador += 1
        
        nuevo_producto = Productos(
            nombre=nombre_copia,
            habilitado=producto_original.habilitado
        )
        db.add(nuevo_producto)
        db.flush()
        
        relaciones_sectores = db.query(ProductosSectores).filter(
            ProductosSectores.id_producto == producto_original.id_producto
        ).all()
        
        for relacion in relaciones_sectores:
            nueva_relacion = ProductosSectores(
                id_producto=nuevo_producto.id_producto,
                id_sector=relacion.id_sector
            )
            db.add(nueva_relacion)
        
        labores = db.query(Labores).filter(
            Labores.id_producto == producto_original.id_producto
        ).all()
        
        for labor in labores:
            nuevo_labor = Labores(
                id_sector=labor.id_sector,
                id_producto=nuevo_producto.id_producto,
                nombre=labor.nombre,
                habilitado=labor.habilitado
            )
            db.add(nuevo_labor)
        
        db.commit()
        db.refresh(nuevo_producto)
        
        return {
            "success": True,
            "detail": "Producto duplicado exitosamente"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
