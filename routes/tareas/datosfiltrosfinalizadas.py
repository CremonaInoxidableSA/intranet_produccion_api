from fastapi import APIRouter, HTTPException, Query
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/filtros", tags=["filtros"])

@router.get("/numeros-op-finalizadas")
def obtener_numeros_op_finalizadas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None)
):
    """Retorna los números de OP existentes con al menos una tarea en estado finalizada.
    
    Parámetros:
        fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
    
    Retorna un array de enteros con los números de OP únicos.
    """
    db = SessionLocal()
    try:
        query = db.query(Tareas.numero_op).filter(
            Tareas.estado == "finalizada"
        )
        
        if fecha_inicio:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Tareas.fecha_fin >= fecha_inicio_dt)
        
        if fecha_fin:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Tareas.fecha_fin <= fecha_fin_dt)
        
        numeros_op = query.distinct().all()
        
        if not numeros_op:
            return {"success": False, "detail": "No existen tareas finalizadas en la base de datos"}

        numeros_op_lista = [op[0] for op in numeros_op]
        
        return {
            "numeros_op": sorted(numeros_op_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/numeros-plano-finalizadas")
def obtener_numeros_plano_finalizadas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None)
):
    """Retorna los números de plano existentes con al menos una tarea en estado finalizada.
    
    Parámetros:
        fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
    
    Retorna un array de strings con los números de plano únicos.
    """
    db = SessionLocal()
    try:
        query = db.query(Tareas.numero_plano).filter(
            Tareas.estado == "finalizada"
        )
        
        if fecha_inicio:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Tareas.fecha_fin >= fecha_inicio_dt)
        
        if fecha_fin:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Tareas.fecha_fin <= fecha_fin_dt)
        
        numeros_plano = query.distinct().all()
        
        numeros_plano_lista = [plano[0] for plano in numeros_plano]
        
        return {
            "numeros_plano": sorted(numeros_plano_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/listado-operarios-finalizadas")
def obtener_listado_operarios_finalizadas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None)
):
    """Retorna los nombres concatenados (apellido + nombre) de los operarios con al menos una tarea en estado finalizada.
    
    Parámetros:
        fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
    
    Retorna un array de strings con formato "apellido+nombre" únicos.
    """
    db = SessionLocal()
    try:
        query = db.query(
            Tareas.apellido_operario_seleccionado,
            Tareas.nombre_operario_seleccionado
        ).filter(
            Tareas.estado == "finalizada"
        )
        
        if fecha_inicio:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Tareas.fecha_fin >= fecha_inicio_dt)
        
        if fecha_fin:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Tareas.fecha_fin <= fecha_fin_dt)
        
        encargados = query.distinct().all()
        
        encargados_lista = [f"{encargado[0]} {encargado[1]}" for encargado in encargados]
        
        return {
            "encargados": sorted(encargados_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/sectores-finalizadas")
def obtener_sectores_finalizadas(
    fecha_inicio: Optional[str] = Query(None),
    fecha_fin: Optional[str] = Query(None)
):
    """Retorna los nombres de los sectores existentes con al menos una tarea en estado finalizada.
    
    Parámetros:
        fecha_inicio: Fecha de inicio (formato: YYYY-MM-DD)
        fecha_fin: Fecha de fin (formato: YYYY-MM-DD)
    
    Retorna un array de strings con los nombres de sectores únicos.
    """
    db = SessionLocal()
    try:
        query = db.query(Sectores.nombre).join(
            Tareas, Tareas.id_sector == Sectores.id_sector
        ).filter(
            Tareas.estado == "finalizada"
        )
        
        if fecha_inicio:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(Tareas.fecha_fin >= fecha_inicio_dt)
        
        if fecha_fin:
            fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")
            fecha_fin_dt = fecha_fin_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Tareas.fecha_fin <= fecha_fin_dt)
        
        sectores = query.distinct().all()
        
        sectores_lista = [sector[0] for sector in sectores]
        
        return {
            "sectores": sorted(sectores_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()