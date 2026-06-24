from fastapi import APIRouter, HTTPException
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from models.productos import Productos
from models.sectores import Sectores
from utils.tiempo_utils import calcular_tiempo_cronometrado, formato_hhmmss

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get("/detalle-tarea-activa")
def obtener_detalle_tarea(id_tarea: int):
    """Obtiene todos los detalles de una tarea específica.
    
    Devuelve todos los campos de la tarea incluyendo los nombres de 
    productos y sectores asociados.
    """
    db = SessionLocal()
    try:
        # Obtener la tarea con sus relaciones
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Verificar que la tarea no esté finalizada
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail=f"Tarea con id {id_tarea} ya se encuentra finalizada")
        
        # Obtener datos relacionados
        producto = db.query(Productos).filter(Productos.id_producto == tarea.id_producto).first() if tarea.id_producto else None
        sector = db.query(Sectores).filter(Sectores.id_sector == tarea.id_sector).first() if tarea.id_sector else None
        
        return {
            "id_tarea": tarea.id_tarea,
            "nombre_operario_seleccionado": tarea.nombre_operario_seleccionado,
            "apellido_operario_seleccionado": tarea.apellido_operario_seleccionado,
            "nombre_sector": sector.nombre if sector else None,
            "numero_op": tarea.numero_op,
            "numero_plano": tarea.numero_plano,
            "nombre_producto": producto.nombre if producto else None,
            "nombre_labor": tarea.nombre_labor,
            "descripcion": tarea.descripcion if tarea.descripcion else "",
            "tiempo_extra": tarea.tiempo_extra if tarea.tiempo_extra else "00:00:00",
            "estado": tarea.estado
            }        

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/tarea-activa-cronometrado")
def obtener_tiempo_cronometrado(id_tarea: int):
    """Obtiene el tiempo cronometrado de una tarea específica en formato HH:MM:SS.
    """
    db = SessionLocal()
    try:
        # Obtener la tarea con sus relaciones
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Calcular tiempo cronometrado
        tiempo_activo_segundos = calcular_tiempo_cronometrado(
            tarea.fecha_inicio,
            tarea.fecha_fin,
            tarea.pausas_reanudaciones
        )
        tiempo_activo_formateado = formato_hhmmss(tiempo_activo_segundos)
        
        return {
            "id_tarea": tarea.id_tarea,
            "tiempo_cronometrado": tiempo_activo_formateado,
            "ultima_actualizacion": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }        

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()