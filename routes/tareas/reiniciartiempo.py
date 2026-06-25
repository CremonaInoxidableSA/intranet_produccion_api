from fastapi import APIRouter, HTTPException
from datetime import datetime
from config.db import SessionLocal
from sqlalchemy import text
from models.tareas import Tareas

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.put("/reiniciar-tiempo-cronometrado")
def reiniciar_tiempo_cronometrado(id_tarea: int):
    """Reinicia el tiempo cronometrado de una tarea específica.
    
    Actualiza:
    - fecha_inicio a la fecha actual
    - pausas_reanudaciones a NULL (limpia pausas)
    
    Validación:
    - La tarea NO debe tener fecha_fin asignada
    """
    db = SessionLocal()
    try:
        # Obtener la tarea
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Verificar que la tarea no esté finalizada
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail="No se puede reiniciar el tiempo de una tarea finalizada")
        
        # Actualizar fecha_inicio y dropear pausas_reanudaciones a NULL
        db.execute(
            text("UPDATE tareas SET fecha_inicio = :fecha_inicio, pausas_reanudaciones = NULL, estado = 'activa' WHERE id_tarea = :id_tarea"),
            {"fecha_inicio": datetime.now(), "id_tarea": id_tarea}
        )
        
        db.commit()
        
        return {
            "id_tarea": tarea.id_tarea,
            "detail": "Tiempo cronometrado reiniciado exitosamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()