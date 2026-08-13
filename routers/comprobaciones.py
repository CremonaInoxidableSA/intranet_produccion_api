from fastapi import APIRouter, HTTPException, Depends
from config.db import SessionLocal
from models.tareas import Tareas
from datetime import datetime

from security.permissions import require_role

router = APIRouter(prefix="/comprobaciones", tags=["comprobaciones"])

@router.get(
    "/tarea-activa-operario",
    dependencies=[Depends(require_role("PERMISO_CREAR_TAREAS_PRODUCCION"))]
)
def verificar_tarea_activa(id_operario: int):
    """Verifica si existe una tarea activa para el operario especificado (por ID).
    """
    db = SessionLocal()
    try:
        tarea = (
            db.query(Tareas)
            .filter(
                Tareas.id_operario_seleccionado == id_operario,
                Tareas.fecha_fin.is_(None),
                Tareas.estado != "pausada"
            )
            .first()
        )
        
        if not tarea:
            return {"success": True}
        
        return {
            "detail": "Existe una tarea activa para el operario seleccionado",
            "success": False,
            "nombre_labor": tarea.nombre_labor,
            "nombre_creador": tarea.nombre_usuario_logeado,
            "apellido_creador": tarea.apellido_usuario_logeado,
            "id_tarea": tarea.id_tarea
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
