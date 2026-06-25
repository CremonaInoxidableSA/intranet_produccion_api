from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from models.productos import Productos
from models.productos_sectores import ProductosSectores

router = APIRouter(prefix="/tareas", tags=["tareas"])

class CrearTareaRequest(BaseModel):
    id_usuario_logeado: int
    nombre_usuario_logeado: str
    apellido_usuario_logeado: str
    id_operario_seleccionado: int
    nombre_operario_seleccionado: str
    apellido_operario_seleccionado: str
    id_sector: int
    numero_op: int
    numero_plano: int
    id_producto: int
    nombre_labor: str
    descripcion: str = ""
    tiempo_extra: str = "00:00:00"

@router.post("/crear-tarea")
def crear_tarea(tarea_data: CrearTareaRequest):
    """Crea una nueva tarea.
    
    Validaciones:
    - id_sector debe existir
    - id_producto debe existir
    - id_producto e id_sector deben estar relacionados en productos_sectores
    - tiempo_extra debe estar en formato HH:MM:SS
    - descripcion no debe superar 255 caracteres
    
    Args:
        tarea_data: Datos de la tarea a crear
    """
    db = SessionLocal()
    try:
        # Verificar que no exista una tarea activa para el operario seleccionado
        tarea_activa = db.query(Tareas).filter(
            Tareas.id_operario_seleccionado == tarea_data.id_operario_seleccionado,
            Tareas.estado == "activa"
        ).first()
        
        if tarea_activa:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Existe una tarea activa para el operario seleccionado"})
        
        sector = db.query(Sectores).filter(Sectores.id_sector == tarea_data.id_sector).first()
        if not sector:
            return JSONResponse(status_code=400, content={"success": False, "detail": f"Sector con id {tarea_data.id_sector} no existe"})
        
        producto = db.query(Productos).filter(Productos.id_producto == tarea_data.id_producto).first()
        if not producto:
            return JSONResponse(status_code=400, content={"success": False, "detail": f"Producto con id {tarea_data.id_producto} no existe"})
        
        producto_sector = db.query(ProductosSectores).filter(
            ProductosSectores.id_producto == tarea_data.id_producto,
            ProductosSectores.id_sector == tarea_data.id_sector
        ).first()
        if not producto_sector:
            return JSONResponse(status_code=400, content={"success": False, "detail": f"El producto con id {tarea_data.id_producto} no está disponible para el sector con id {tarea_data.id_sector}"})
        
        partes = tarea_data.tiempo_extra.split(":")
        if len(partes) != 3:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Formato tiempo_extra inválido. Debe ser HH:MM:SS"})
        
        try:
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])
            
            if not (0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59):
                raise ValueError("Valores fuera de rango")
        except ValueError:
            return JSONResponse(status_code=400, content={"success": False, "detail": "Formato tiempo_extra inválido. Valores no numéricos o fuera de rango"})
        
        if len(tarea_data.descripcion) > 255:
            return JSONResponse(status_code=400, content={"success": False, "detail": "La descripción no puede superar 255 caracteres."})
        
        nueva_tarea = Tareas(
            id_usuario_logeado=tarea_data.id_usuario_logeado,
            nombre_usuario_logeado=tarea_data.nombre_usuario_logeado,
            apellido_usuario_logeado=tarea_data.apellido_usuario_logeado,
            id_operario_seleccionado=tarea_data.id_operario_seleccionado,
            nombre_operario_seleccionado=tarea_data.nombre_operario_seleccionado,
            apellido_operario_seleccionado=tarea_data.apellido_operario_seleccionado,
            numero_op=tarea_data.numero_op,
            numero_plano=tarea_data.numero_plano,
            id_sector=tarea_data.id_sector,
            id_producto=tarea_data.id_producto,
            nombre_labor=tarea_data.nombre_labor,
            descripcion=tarea_data.descripcion,
            fecha_inicio=datetime.now(),
            tiempo_extra=tarea_data.tiempo_extra,
            estado="activa"
        )
        
        db.add(nueva_tarea)
        db.commit()
        db.refresh(nueva_tarea)
        
        return {
            "success": True,
            "detail": "Tarea creada correctamente",
            "id_tarea": nueva_tarea.id_tarea
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"success": False, "detail": f"Error interno del servidor: {str(e)}"})
    finally:
        db.close()
