from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from models.productos import Productos
from sqlalchemy import func
from utils.tiempo_utils import calcular_tiempo_cronometrado, formato_hhmmss

from security.permissions import require_role

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get(
    "/operarios-estado",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_PANEL_PRODUCCION"))]
)
def obtener_operarios_estado():
    """
    Retorna un listado de cada operario y su estado de tareas.
    """
    db = SessionLocal()
    try:
        operarios_unicos = db.query(
            Tareas.id_operario_seleccionado,
            Tareas.nombre_operario_seleccionado,
            Tareas.apellido_operario_seleccionado
        ).distinct().all()
        
        operarios_data = []
        total_activos = 0
        total_inactivos = 0
        
        for op_id, op_nombre, op_apellido in operarios_unicos:
            # Buscar tarea activa para este operario
            tarea_activa = db.query(Tareas).filter(
                Tareas.id_operario_seleccionado == op_id,
                Tareas.estado == "activa"
            ).first()
            
            # Contar tareas pausadas
            tareas_pausadas = db.query(func.count(Tareas.id_tarea)).filter(
                Tareas.id_operario_seleccionado == op_id,
                Tareas.estado == "pausada"
            ).scalar() or 0
            
            operario_info = {
                "nombre_operario": op_nombre,
                "apellido_operario": op_apellido,
                "numero_tareas_pausa": tareas_pausadas
            }
            
            if tarea_activa:
                # Calcular tiempo cronometrado
                tiempo_crono = calcular_tiempo_cronometrado(
                    tarea_activa.fecha_inicio,
                    tarea_activa.fecha_fin,
                    tarea_activa.pausas_reanudaciones
                )
                
                # Obtener datos del sector
                sector_nombre = ""
                if tarea_activa.id_sector:
                    sector = db.query(Sectores).filter(
                        Sectores.id_sector == tarea_activa.id_sector
                    ).first()
                    sector_nombre = sector.nombre if sector else ""
                
                # Obtener datos del producto
                producto_nombre = ""
                if tarea_activa.id_producto:
                    producto = db.query(Productos).filter(
                        Productos.id_producto == tarea_activa.id_producto
                    ).first()
                    producto_nombre = producto.nombre if producto else ""
                
                operario_info.update({
                    "estado": "activa",
                    "numero_op": tarea_activa.numero_op,
                    "sector": sector_nombre,
                    "producto": producto_nombre,
                    "tiempo_cronometrado": formato_hhmmss(tiempo_crono)
                })
                total_activos += 1
            else:
                operario_info["estado"] = "inactivo"
                total_inactivos += 1
            
            operarios_data.append(operario_info)
        
        return {
            "success": True,
            "operarios": operarios_data,
            "total_operarios_activos": total_activos,
            "total_operarios_inactivos": total_inactivos
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
