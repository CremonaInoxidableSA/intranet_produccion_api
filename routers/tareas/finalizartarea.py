from fastapi import APIRouter, HTTPException
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from utils.tiempo_utils import calcular_tiempo_cronometrado, formato_hhmmss, hhmmss_a_segundos

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.post("/finalizar-tarea")
def finalizar_tarea(id_tarea: int):
    """Finaliza una tarea específica.
    
    Operaciones:
    - Asigna fecha_fin a la fecha actual
    - Calcula tiempo_cronometrado usando la función de tiempo_utils
    - Obtiene tiempo_extra de la BD (formato HH:MM:SS) y lo suma al tiempo cronometrado
    - Guarda el resultado en tiempo_total (formato HH:MM:SS)
    - Actualiza estado a "finalizada"
    
    Args:
        id_tarea (int): ID de la tarea a finalizar
    """
    db = SessionLocal()
    try:
        # Obtener la tarea
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Verificar que la tarea no esté ya finalizada
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail=f"Tarea con id {id_tarea} ya se encuentra finalizada")
        
        # Asignar fecha_fin
        fecha_fin_actual = datetime.now()
        tarea.fecha_fin = fecha_fin_actual
        
        # Calcular tiempo cronometrado
        tiempo_cronometrado_segundos = calcular_tiempo_cronometrado(
            tarea.fecha_inicio,
            fecha_fin_actual,
            tarea.pausas_reanudaciones
        )
        
        # Obtener tiempo_extra de la BD y convertir a segundos
        tiempo_extra_str = tarea.tiempo_extra if tarea.tiempo_extra else "00:00:00"
        tiempo_extra_segundos = hhmmss_a_segundos(tiempo_extra_str)
        duracion_total_segundos = tiempo_cronometrado_segundos + tiempo_extra_segundos
        
        # Convertir duracion_total a formato HH:MM:SS
        duracion_formateada = formato_hhmmss(duracion_total_segundos)
        tiempo_cronometrado_formateado = formato_hhmmss(tiempo_cronometrado_segundos)
        
        # Actualizar campos
        tarea.tiempo_cronometrado = tiempo_cronometrado_formateado
        tarea.tiempo_total = duracion_formateada
        tarea.estado = "finalizada"
        
        db.commit()
        
        return {
            "id_tarea": tarea.id_tarea,
            "detail": "Tarea finalizada correctamente"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
