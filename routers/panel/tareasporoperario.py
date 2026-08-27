from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import httpx
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from models.productos import Productos
from sqlalchemy import func
from utils.tiempo_utils import calcular_tiempo_cronometrado, formato_hhmmss

from security.permissions import require_role
from security.dependencies import get_current_user
from schemas.authenticated_user import AuthenticatedUser

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get(
    "/operarios-estado",
    dependencies=[Depends(require_role("PERMISO_CONSULTAR_PANEL_PRODUCCION"))]
)
async def obtener_operarios_estado(
    current_user: AuthenticatedUser = Depends(get_current_user),
    request: Request = None
):
    """
    Retorna un listado de cada operario y su estado de tareas.
    Obtiene la lista completa de operarios desde la API externa.
    """
    db = SessionLocal()
    try:
        # Obtener el token JWT del header Authorization
        auth_header = request.headers.get("authorization", "")
        
        headers = {
            "Authorization": auth_header
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://apikeycloak.intranetcreminox.com/usuarios-produccion/lista?filtro=0",
                headers=headers
            )
            response.raise_for_status()
            operarios_externos = response.json()
        
        operarios_data = []
        total_activos = 0
        total_inactivos = 0
        
        for operario_ext in operarios_externos:
            op_id = operario_ext["id"]
            op_nombre = operario_ext["nombre"]
            op_apellido = operario_ext["apellido"]
            
            operario_info = {
                "nombre_operario": op_nombre,
                "apellido_operario": op_apellido,
                "numero_tareas_pausa": 0
            }
            
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
            
            operario_info["numero_tareas_pausa"] = tareas_pausadas
            
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
            "operarios": operarios_data,
            "total_operarios_activos": total_activos,
            "total_operarios_inactivos": total_inactivos
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
