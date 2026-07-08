from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from config.db import SessionLocal
from models.productos import Productos
from models.productos_sectores import ProductosSectores
from models.sectores import Sectores

class CrearProductoRequest(BaseModel):
    nombre: str
    id_sectores: List[int]

router = APIRouter(prefix="/productos", tags=["productos"])

@router.post("/crear-producto")
def crear_producto(data: CrearProductoRequest):
    """Crea un nuevo producto y lo asigna a los sectores especificados.
    
    Parámetros:
    - nombre: string, nombre del producto
    - id_sectores: array de enteros, ids de los sectores a asignar
    """
    db = SessionLocal()
    try:
        if not data.nombre or data.nombre.strip() == "":
            raise HTTPException(status_code=400, detail="El nombre del producto no puede estar vacío")
        
        if data.nombre and data.nombre.strip() == "Otro":
            raise HTTPException(status_code=400, detail="El nombre del producto no puede ser 'Otro'")

        if not data.id_sectores or len(data.id_sectores) == 0:
            raise HTTPException(status_code=400, detail="Debe asignar al menos un sector al producto")
        
        # Verificar que todos los sectores existan en la tabla de sectores
        sectores_validos = db.query(Sectores.id_sector).filter(
            Sectores.id_sector.in_(data.id_sectores)
        ).all()
        
        ids_validos = {s[0] for s in sectores_validos}
        ids_solicitados = set(data.id_sectores)
        
        sectores_invalidos = ids_solicitados - ids_validos
        if sectores_invalidos:
            raise HTTPException(
                status_code=400, 
                detail=f"Los siguientes sectores no existen: {list(sectores_invalidos)}"
            )
        
        nuevo_producto = Productos(
            nombre=data.nombre.strip()
        )
        db.add(nuevo_producto)
        db.flush()  # Flush para obtener el id antes de hacer commit
        
        for id_sector in data.id_sectores:
            relacion = ProductosSectores(
                id_producto=nuevo_producto.id_producto,
                id_sector=id_sector
            )
            db.add(relacion)
        
        db.commit()
        db.refresh(nuevo_producto)
        
        return {
            "id_producto": nuevo_producto.id_producto,
            "nombre": nuevo_producto.nombre,
            "detail": "Producto creado exitosamente"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
