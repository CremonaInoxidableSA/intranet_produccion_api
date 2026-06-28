from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores

router = APIRouter(prefix="/filtros", tags=["filtros"])

@router.get("/numeros-op-finalizadas")
def obtener_numeros_op_finalizadas():
    """Retorna los números de OP existentes con al menos una tarea en estado finalizada.
    
    Retorna un array de enteros con los números de OP únicos.
    """
    db = SessionLocal()
    try:
        numeros_op = db.query(Tareas.numero_op).filter(
            Tareas.estado == "finalizada"
        ).distinct().all()
        
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
def obtener_numeros_plano_finalizadas():
    """Retorna los números de plano existentes con al menos una tarea en estado finalizada.
    
    Retorna un array de strings con los números de plano únicos.
    """
    db = SessionLocal()
    try:
        numeros_plano = db.query(Tareas.numero_plano).filter(
            Tareas.estado == "finalizada"
        ).distinct().all()
        
        numeros_plano_lista = [plano[0] for plano in numeros_plano]
        
        return {
            "numeros_plano": sorted(numeros_plano_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/listado-operarios-finalizadas")
def obtener_listado_operarios_finalizadas():
    """Retorna los nombres concatenados (apellido + nombre) de los operarios con al menos una tarea en estado finalizada.
    
    Retorna un array de strings con formato "apellido+nombre" únicos.
    """
    db = SessionLocal()
    try:
        encargados = db.query(
            Tareas.apellido_operario_seleccionado,
            Tareas.nombre_operario_seleccionado
        ).filter(
            Tareas.estado == "finalizada"
        ).distinct().all()
        
        encargados_lista = [f"{encargado[0]} {encargado[1]}" for encargado in encargados]
        
        return {
            "encargados": sorted(encargados_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/sectores-finalizadas")
def obtener_sectores_finalizadas():
    """Retorna los nombres de los sectores existentes con al menos una tarea en estado finalizada.
    
    Retorna un array de strings con los nombres de sectores únicos.
    """
    db = SessionLocal()
    try:
        sectores = db.query(Sectores.nombre).join(
            Tareas, Tareas.id_sector == Sectores.id_sector
        ).filter(
            Tareas.estado == "finalizada"
        ).distinct().all()
        
        sectores_lista = [sector[0] for sector in sectores]
        
        return {
            "sectores": sorted(sectores_lista)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()