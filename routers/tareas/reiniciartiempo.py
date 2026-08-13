from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from config.db import SessionLocal
from models.tareas import Tareas

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.put("/reiniciar-tiempo-cronometrado")
def reiniciar_tiempo_cronometrado(id_tarea: int):
    """Reinicia el tiempo cronometrado de una tarea específica.
    
    Actualiza:
    - fecha_inicio a la fecha actual
    
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
        
        # Capturar el tiempo una sola vez para garantizar consistencia
        ahora = datetime.now()
        tiempo_formateado = ahora.strftime("%Y-%m-%d %H:%M:%S")
        
        # Actualizar fecha_inicio, pausas_reanudaciones y estado
        tarea.fecha_inicio = tiempo_formateado
        tarea.pausas_reanudaciones = [tiempo_formateado]
        tarea.estado = "pausada"
        
        db.commit()
        db.refresh(tarea)
        
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