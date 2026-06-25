from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from models.modificaciones import Modificaciones

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.delete("/eliminar-tarea")
def eliminar_tarea(id_tarea: int):
    """Elimina una tarea y todos los registros de modificaciones asociados.
    
    Este endpoint elimina:
    1. Todos los registros en la tabla 'modificaciones' que referencian el id_tarea
    2. El registro de la tarea en la tabla 'tareas'
    """
    db = SessionLocal()
    try:
        # Buscar la tarea
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con ID {id_tarea} no encontrada")
        
        # Eliminar todos los registros de modificaciones asociados a esta tarea
        db.query(Modificaciones).filter(Modificaciones.id_tarea == id_tarea).delete()
        
        # Eliminar la tarea
        db.delete(tarea)
        db.commit()
        
        return {
            "estado": "eliminada",
            "detail": f"Tarea {id_tarea} y sus modificaciones fueron eliminadas correctamente"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
