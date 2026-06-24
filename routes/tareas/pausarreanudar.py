from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from datetime import datetime
from sqlalchemy.orm.attributes import flag_modified

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.post("/pausar-tarea")
def pausar_tarea(id_tarea: int):
    """Pausa una tarea agregando el timestamp actual al array pausas_reanudaciones.
    
    La tarea debe estar ACTIVA (número PAR de pausas_reanudaciones o NULL/0).
    No se puede pausar una tarea finalizada o ya pausada.
    """
    db = SessionLocal()
    try:
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con ID {id_tarea} no encontrada")
        
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail="No se puede pausar una tarea finalizada")
        
        # Verificar si la tarea está activa (número PAR de elementos = ACTIVA)
        pausas_reanudaciones = tarea.pausas_reanudaciones
        if pausas_reanudaciones is None or len(pausas_reanudaciones) == 0:
            # Tarea activa, puede pausarse
            esta_activa = True
        else:
            # Número impar de elementos = tarea pausada, número par = tarea activa
            esta_activa = len(pausas_reanudaciones) % 2 == 0
        
        if not esta_activa:
            raise HTTPException(status_code=400, detail="La tarea ya está pausada, no se puede pausar nuevamente")
        
        # Inicializar o agregar al array pausas_reanudaciones
        pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
        pausas.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tarea.pausas_reanudaciones = pausas
        flag_modified(tarea, "pausas_reanudaciones")
        tarea.estado = "pausada"
        
        db.commit()
        db.refresh(tarea)
        
        return {
            "estado": "pausada",
            "mensaje": "Tarea pausada correctamente",
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()


@router.post("/reanudar-tarea")
def reanudar_tarea(id_tarea: int):
    """Reanuda una tarea agregando el timestamp actual al array pausas_reanudaciones.
    
    La tarea debe estar PAUSADA (número IMPAR de pausas_reanudaciones).
    No se puede reanudar una tarea finalizada o que ya está en ejecución.
    """
    db = SessionLocal()
    try:
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con ID {id_tarea} no encontrada")
        
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail="No se puede reanudar una tarea finalizada")
        
        pausas_reanudaciones = tarea.pausas_reanudaciones
        
        if pausas_reanudaciones is None or len(pausas_reanudaciones) == 0:
            raise HTTPException(status_code=400, detail="La tarea ya está en ejecución")
        
        # Verificar si la tarea está pausada (número IMPAR de elementos = PAUSADA)
        esta_pausada = len(pausas_reanudaciones) % 2 == 1
        
        if not esta_pausada:
            raise HTTPException(status_code=400, detail="La tarea ya está en ejecución")
        
        # Agregar el timestamp actual
        pausas = tarea.pausas_reanudaciones
        pausas.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tarea.pausas_reanudaciones = pausas
        flag_modified(tarea, "pausas_reanudaciones")
        tarea.estado = "activa"
        
        db.commit()
        db.refresh(tarea)
        
        return {
            "estado": "activa",
            "mensaje": "Tarea reanudada correctamente"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()