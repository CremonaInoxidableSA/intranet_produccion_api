from fastapi import APIRouter, HTTPException
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from models.productos import Productos
from models.sectores import Sectores
from utils.tiempo_utils import calcular_tiempo_cronometrado, formato_hhmmss

router = APIRouter(prefix="/tareas", tags=["tareas"])

def procesar_eventos(pausas_reanudaciones):
    """Procesa el array de pausas_reanudaciones y lo convierte en un array de eventos.
    
    Estructura esperada de pausas_reanudaciones:
    - Array de objetos con estructura {"datetime": "...", "type": "pausa|reanudacion"}
    - O array alternado donde índices pares son pausas e impares son reanudaciones
    
    Retorna un array de objetos con estructura {fecha": "...", "titulo": "pausa|reanudacion"}
    Si no existe o está vacío, retorna []
    """
    if not pausas_reanudaciones:
        return []
    
    eventos = []
    
    for index, evento in enumerate(pausas_reanudaciones):
        # Si el evento tiene un campo "type", usarlo; si no, alternar pausa/reanudacion
        if isinstance(evento, dict):
            datetime_str = evento.get("datetime") or evento.get("timestamp") or str(evento)
            
            # Determinar el tipo de evento
            if "type" in evento:
                tipo = evento["type"]
            else:
                # Alternar: pausa en índices pares, reanudación en impares
                tipo = "pausa" if index % 2 == 0 else "reanudacion"
        else:
            # Si es un string o timestamp directo
            datetime_str = str(evento)
            tipo = "pausa" if index % 2 == 0 else "reanudacion"
        
        eventos.append({
            "fecha": datetime_str,
            "titulo": tipo
        })
    
    return eventos

@router.get("/detalle-tarea-finalizada-general")
def obtener_detalle_tarea_finalizada_general(id_tarea: int):
    """Obtiene todos los detalles de una tarea específica. Esta consulta es utilizada
    en el sector denominado "DETALLE TAREA FINALIZADA" del sector "MONITOREO".
    """
    db = SessionLocal()
    try:
        # Obtener la tarea con sus relaciones
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        
        if not tarea:
            raise HTTPException(status_code=404, detail=f"Tarea con id {id_tarea} no encontrada")
        
        # Verificar que la tarea esté finalizada
        if tarea.fecha_fin is None or tarea.estado != "finalizada":
            raise HTTPException(status_code=400, detail=f"Tarea con id {id_tarea} no se encuentra finalizada")
        
        # Obtener datos relacionados
        producto = db.query(Productos).filter(Productos.id_producto == tarea.id_producto).first() if tarea.id_producto else None
        sector = db.query(Sectores).filter(Sectores.id_sector == tarea.id_sector).first() if tarea.id_sector else None
        
        return {
            "id_tarea": tarea.id_tarea,
            "fecha_inicio": tarea.fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_fin": tarea.fecha_fin.strftime("%Y-%m-%d %H:%M:%S"),
            "apellido_creador": tarea.apellido_usuario_logeado,
            "nombre_creador": tarea.nombre_usuario_logeado,
            "apellido_operario_seleccionado": tarea.apellido_operario_seleccionado,
            "nombre_operario_seleccionado": tarea.nombre_operario_seleccionado,
            "nombre_sector": sector.nombre if sector else None,
            "numero_op": tarea.numero_op,
            "numero_plano": tarea.numero_plano,
            "nombre_producto": producto.nombre if producto else None,
            "nombre_labor": tarea.nombre_labor,
            "descripcion": tarea.descripcion if tarea.descripcion else "",
            "tiempo_extra": tarea.tiempo_extra if tarea.tiempo_extra else "00:00:00",
            "tiempo_cronometrado": tarea.tiempo_cronometrado,
            "tiempo_total": tarea.tiempo_total,
            "eventos": procesar_eventos(tarea.pausas_reanudaciones)
        }        

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()