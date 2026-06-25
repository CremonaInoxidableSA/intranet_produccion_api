from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from models.tareas import Tareas

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.put("/actualizar-tiempo-extra")
def actualizar_tiempo_extra(id_tarea: int, tiempo_extra: str):
    """Actualiza el tiempo_extra de una tarea específica.
    
    Args:
        id_tarea (int): ID de la tarea
        tiempo_extra (str): Tiempo extra en formato HH:MM:SS
    """
    db = SessionLocal()
    try:
        # Obtener la tarea
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            return JSONResponse(status_code=404, content={"success": False, "detail": f"Tarea con id {id_tarea} no encontrada"})
        
        # Verificar que la tarea no esté finalizada
        if tarea.fecha_fin is not None:
            return JSONResponse(status_code=400, content={"success": False, "detail": "No se puede modificar una tarea finalizada"})
        
        # Validar formato HH:MM:SS
        partes = tiempo_extra.split(":")
        if len(partes) != 3:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Formato inválido. Debe ser HH:MM:SS"})
        
        try:
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])
            
            if not (0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59):
                raise ValueError("Valores fuera de rango")
        except ValueError:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Formato inválido. Valores no numéricos o fuera de rango"})
        
        # Actualizar campo
        tarea.tiempo_extra = tiempo_extra
        
        db.commit()
        
        return {
            "success": True,
            "id_tarea": tarea.id_tarea,
            "detail": "Tiempo extra actualizado correctamente"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"success": False, "detail": f"Error interno del servidor: {str(e)}"})
    finally:
        db.close()


@router.put("/actualizar-descripcion")
def actualizar_descripcion(id_tarea: int, descripcion: str):
    """Actualiza la descripción de una tarea específica.
    
    Args:
        id_tarea (int): ID de la tarea
        descripcion (str): Nueva descripción (máximo 255 caracteres)
    """
    db = SessionLocal()
    try:
        # Obtener la tarea
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Verificar que la tarea no esté finalizada
        if tarea.fecha_fin is not None:
            raise HTTPException(status_code=400, detail="No se puede modificar una tarea finalizada")
        
        # Validar longitud de descripción
        if len(descripcion) > 255:
            raise HTTPException(status_code=400, detail=f"La descripción no puede superar 255 caracteres")
        
        # Actualizar campo
        tarea.descripcion = descripcion
        
        db.commit()
        
        return {
            "id_tarea": tarea.id_tarea,
            "detail": "Descripción actualizada correctamente"
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
