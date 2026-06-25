from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from models.labores import Labores
from datetime import datetime

router = APIRouter(prefix="/comprobaciones", tags=["comprobaciones"])

@router.get("/tarea-activa-operario")
def verificar_tarea_activa(id_operario: int):
    """Verifica si existe una tarea activa para el operario especificado (por ID).
    
    Una tarea se considera activa si:
    - No tiene fecha_fin (fecha_fin IS NULL)
    - El último elemento en pausas_reanudaciones tiene índice PAR (no está pausada)
    
    Si existe tarea activa retorna los datos, si no retorna disponibilidad.
    """
    db = SessionLocal()
    try:
        # Buscar tarea activa para el operario (sin fecha_fin)
        tarea = (
            db.query(Tareas, Labores)
            .join(Labores, Tareas.id_labor == Labores.id_labor)
            .filter(
                Tareas.id_operario_seleccionado == id_operario,
                Tareas.fecha_fin.is_(None)
            )
            .first()
        )
        
        if not tarea:
            return {"detail": "El operario se encuentra disponible"}
        
        tarea_obj, labor_obj = tarea
        pausas_reanudaciones = tarea_obj.pausas_reanudaciones
        
        # Verificar si la tarea está pausada o activa
        # Si el array está vacío o es NULL, la tarea está activa
        # Posición 0 = Primera pausa, Posición 1 = Primera reanudación, etc.
        # Si el número de elementos es IMPAR, el último índice es PAR (pausa) → PAUSADA
        # Si el número de elementos es PAR, el último índice es IMPAR (reanudación) → ACTIVA
        if pausas_reanudaciones is None or len(pausas_reanudaciones) == 0:
            # Tarea activa, nunca ha sido pausada
            esta_pausada = False
        else:
            # Número impar de elementos = tarea pausada
            esta_pausada = len(pausas_reanudaciones) % 2 == 1
        
        if esta_pausada:
            # Si está pausada, no se considera "activa" en el sentido de que está trabajando
            return {"detail": "El operario se encuentra disponible"}
        
        # La tarea está activa (sin pausa)
        return {
            "detail": "Existe una tarea activa para el operario seleccionado",
            "nombre_labor": labor_obj.nombre,
            "nombre_usuario_logeado": tarea_obj.nombre_usuario_logeado,
            "apellido_usuario_logeado": tarea_obj.apellido_usuario_logeado,
            "id_tarea": tarea_obj.id_tarea
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
