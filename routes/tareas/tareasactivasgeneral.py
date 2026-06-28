from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from models.productos import Productos
from sqlalchemy import and_, or_

router = APIRouter(prefix="/tareas", tags=["tareas"])

class FiltrosTareasActivas(BaseModel):
    numeros_op: list[int]
    numeros_plano: list[str]
    operarios: list[str]
    sectores: list[str]

@router.post("/tareas-activas-general")
def obtener_tareas_activas_general(filtros: FiltrosTareasActivas):
    """Retorna un listado de tareas con estado activa o pausada según los filtros proporcionados.
    
    Filtros:
    - numeros_op: Array de int. Si contiene 0, selecciona TODOS los números de OP
    - numeros_plano: Array de string. Si contiene "0", selecciona TODOS los números de plano
    - operarios: Array de string (formato "apellido nombre"). Si contiene "0", selecciona TODOS los operarios
    - sectores: Array de string. Si contiene "0", selecciona TODOS los sectores
    """
    db = SessionLocal()
    try:
        query = db.query(Tareas).filter(
            Tareas.estado.in_(["activa", "pausada"])
        )
        
        # Filtro por números de OP
        if filtros.numeros_op and 0 not in filtros.numeros_op:
            query = query.filter(Tareas.numero_op.in_(filtros.numeros_op))
        
        # Filtro por números de plano
        if filtros.numeros_plano and "0" not in filtros.numeros_plano:
            query = query.filter(Tareas.numero_plano.in_(filtros.numeros_plano))
        
        # Filtro por operarios (apellido + nombre)
        if filtros.operarios and "0" not in filtros.operarios:
            operarios_filtro = []
            for operario in filtros.operarios:
                # Esperamos formato "apellido nombre"
                partes = operario.split(" ", 1)
                if len(partes) == 2:
                    apellido, nombre = partes
                    operarios_filtro.append(
                        and_(
                            Tareas.apellido_operario_seleccionado == apellido,
                            Tareas.nombre_operario_seleccionado == nombre
                        )
                    )
            if operarios_filtro:
                query = query.filter(or_(*operarios_filtro))
        
        # Filtro por sectores
        if filtros.sectores and "0" not in filtros.sectores:
            sectores_ids = db.query(Sectores.id_sector).filter(
                Sectores.nombre.in_(filtros.sectores)
            ).all()
            sectores_ids_list = [s[0] for s in sectores_ids]
            if sectores_ids_list:
                query = query.filter(Tareas.id_sector.in_(sectores_ids_list))
        
        tareas = query.all()
        
        if not tareas:
            return {
                "success": False,
                "detail": "No existen tareas que cumplan con los filtros especificados"
            }
        
        tareas_data = []
        for tarea in tareas:
            producto = db.query(Productos).filter(Productos.id_producto == tarea.id_producto).first() if tarea.id_producto else None
            tareas_data.append({
                "id_tarea": tarea.id_tarea,
                "nombre_operario_seleccionado": tarea.nombre_operario_seleccionado,
                "apellido_operario_seleccionado": tarea.apellido_operario_seleccionado,
                "nombre_producto": producto.nombre if producto else None,
                "nombre_labor": tarea.nombre_labor,
                "estado": tarea.estado
            })
        
        return {
            "success": True,
            "tareas": tareas_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
