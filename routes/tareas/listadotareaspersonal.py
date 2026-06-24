from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.tareas import Tareas
from models.productos import Productos

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get("/listado-tareas-personal")
def obtener_tareas_usuario(id_current_user: int):
    """Obtiene las tareas activas (sin fecha_fin) del usuario actual.
    
    Retorna todas las tareas asignadas al usuario que aún no han sido finalizadas.
    """
    db = SessionLocal()
    try:
        # Obtener tareas sin fecha_fin asignadas al usuario actual
        tareas = db.query(Tareas).filter(
            Tareas.id_operario_seleccionado == id_current_user,
            Tareas.fecha_fin == None
        ).all()
        
        if not tareas:
            return {
                "mensaje": f"No hay tareas activas para el usuario"
            }
        
        tareas_data = []
        for tarea in tareas:
            producto = db.query(Productos).filter(Productos.id_producto == tarea.id_producto).first() if tarea.id_producto else None
            
            tareas_data.append({
                "id_tarea": tarea.id_tarea,
                "nombre_operario_seleccionado": tarea.nombre_operario_seleccionado,
                "apellido_operario_seleccionado": tarea.apellido_operario_seleccionado,
                "nombre_producto": producto.nombre if producto else None,
                "nombre_labor": tarea.nombre_labor
            })
        
        return {
            "tareas": tareas_data
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
