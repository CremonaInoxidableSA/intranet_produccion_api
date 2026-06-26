from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config.db import SessionLocal
from models.labores import Labores

class EliminarLabor(BaseModel):
    id_labor: int

router = APIRouter(prefix="/labores", tags=["labores"])

@router.post("/eliminar-labor")
def eliminar_labor(data: EliminarLabor):
    """Elimina una labor si existe."""
    db = SessionLocal()
    try:
        labor = db.query(Labores).filter(Labores.id_labor == data.id_labor).first()
        
        if not labor:
            return JSONResponse(status_code=404, content={"success": False, "detail": f"Labor con id {data.id_labor} no encontrada"})
        
        if labor.habilitado == False:
            return {
                "detail": "La labor ya está eliminada",
                "success": False
            }

        labor.habilitado = False
        db.commit()
        
        return {
            "detail": "Labor eliminada exitosamente",
            "success": True
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()