from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.labores import Labores
from models.productos_sectores import ProductosSectores

class CrearLaborRequest(BaseModel):
    nombre: str
    id_sector: int
    id_producto: int 

router = APIRouter(prefix="/labores", tags=["labores"])

@router.post("/crear-labor")
def crear_labor(data: CrearLaborRequest):
    """Crea un nuevo labor.
    
    Parámetros:
    - nombre: string, nombre del labor
    - id_sector: integer, id del sector
    - id_producto: integer, id del producto
    
    Validaciones:
    - El nombre no puede estar vacío
    - Debe asignarse un id_sector
    - Debe asignarse un id_producto
    - El producto y sector deben estar relacionados en la tabla productos_sectores
    """
    db = SessionLocal()
    try:
        # Validar que el nombre no esté vacío
        if not data.nombre or data.nombre.strip() == "":
            return JSONResponse(status_code=400, content={"success": False, "detail": "El nombre del labor no puede estar vacío"})
        
        # Validar que id_sector sea proporcionado
        if data.id_sector is None:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Debe asignar un sector al labor"})
        
        # Validar que id_producto sea proporcionado
        if data.id_producto is None:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Debe asignar un producto al labor"})
        
        # Verificar que exista la relación válida entre producto y sector
        relacion_valida = db.query(ProductosSectores).filter(
            ProductosSectores.id_producto == data.id_producto,
            ProductosSectores.id_sector == data.id_sector
        ).first()
        
        if not relacion_valida:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": f"El producto {data.id_producto} no está asignado al sector {data.id_sector}"}
            )
        
        # Crear el nuevo labor con habilitado=True
        nuevo_labor = Labores(
            nombre=data.nombre.strip(),
            id_sector=data.id_sector,
            id_producto=data.id_producto,
            habilitado=True
        )
        db.add(nuevo_labor)
        db.commit()
        db.refresh(nuevo_labor)
        
        return {
            "id_labor": nuevo_labor.id_labor,
            "nombre": nuevo_labor.nombre,
            "id_sector": nuevo_labor.id_sector,
            "id_producto": nuevo_labor.id_producto,
            "habilitado": nuevo_labor.habilitado,
            "detail": "Labor creado exitosamente"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
