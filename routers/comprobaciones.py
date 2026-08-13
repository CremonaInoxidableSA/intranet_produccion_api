from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from datetime import datetime

router = APIRouter(prefix="/comprobaciones", tags=["comprobaciones"])

@router.get("/tarea-activa-operario")
def verificar_tarea_activa(id_operario: int):
    """Verifica si existe una tarea activa para el operario especificado (por ID).
    
    Una tarea se considera activa si:
    - No tiene fecha_fin (fecha_fin IS NULL)
    - El estado es diferente a 'pausada'
    
    Si existe tarea activa retorna los datos, si no retorna disponibilidad.
    """
    db = SessionLocal()
    try:
        # Buscar tarea activa para el operario (sin fecha_fin y no pausada)
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
        
        # La tarea está activa (sin pausa)
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
