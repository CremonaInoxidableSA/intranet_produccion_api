from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func
from config.db import SessionLocal
from models.labores import Labores

from security.permissions import require_role

class ActualizarNombreLaborRequest(BaseModel):
    id_labor: int
    nombre: str

router = APIRouter(prefix="/labores", tags=["labores"])

@router.put(
    "/actualizar-nombre-labor",
    dependencies=[Depends(require_role("PERMISO_ACTUALIZAR_LABORES_PRODUCCION"))]
)
def actualizar_nombre_labor(data: ActualizarNombreLaborRequest):
    """Actualiza el nombre de un labor.
    """
    db = SessionLocal()
    try:
        if not data.nombre or data.nombre.strip() == "":
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "El nombre del labor no puede estar vacío"}
            )
        
        labor = db.query(Labores).filter(
            Labores.id_labor == data.id_labor
        ).first()
        
        if not labor:
            return JSONResponse(
                status_code=404,
                content={"success": False, "detail": f"El labor con id {data.id_labor} no existe"}
            )
        
        nombre_nuevo = data.nombre.strip()
        
        if func.lower(labor.nombre) == func.lower(nombre_nuevo):
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "El nuevo nombre es igual al nombre actual del labor"}
            )
        
        labor_existente = db.query(Labores).filter(
            func.lower(Labores.nombre) == func.lower(nombre_nuevo),
            Labores.id_producto == labor.id_producto,
            Labores.id_labor != data.id_labor,
            Labores.habilitado == True
        ).first()
        
        if labor_existente:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "Ya existe otro labor con el mismo nombre para este producto"}
            )
        
        # Actualizar el nombre
        labor.nombre = nombre_nuevo
        db.commit()
        db.refresh(labor)
        
        return {
            "id_labor": labor.id_labor,
            "nombre": labor.nombre,
            "success": True,
            "detail": "Nombre del labor actualizado exitosamente"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
