from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from models.sectores import Sectores
from models.productos import Productos

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
    - tiempo_extra debe estar en formato HH:MM:SS
    - descripcion no debe superar 255 caracteres
    
    Args:
        tarea_data: Datos de la tarea a crear
    """
    db = SessionLocal()
    try:
        # Validar que id_sector exista
        sector = db.query(Sectores).filter(Sectores.id_sector == tarea_data.id_sector).first()
        if not sector:
            raise HTTPException(status_code=400, detail=f"Sector con id {tarea_data.id_sector} no existe")
        
        # Validar que id_producto exista
        producto = db.query(Productos).filter(Productos.id_producto == tarea_data.id_producto).first()
        if not producto:
            raise HTTPException(status_code=400, detail=f"Producto con id {tarea_data.id_producto} no existe")
        
        # Validar formato HH:MM:SS de tiempo_extra
        partes = tarea_data.tiempo_extra.split(":")
        if len(partes) != 3:
            raise HTTPException(status_code=400, detail="Formato tiempo_extra inválido. Debe ser HH:MM:SS")
        
        try:
            horas = int(partes[0])
            minutos = int(partes[1])
            segundos = int(partes[2])
            
            if not (0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59):
                raise ValueError("Valores fuera de rango")
        except ValueError:
            raise HTTPException(status_code=400, detail="Formato tiempo_extra inválido. Valores no numéricos o fuera de rango")
        
        # Validar longitud de descripción
        if len(tarea_data.descripcion) > 255:
            raise HTTPException(status_code=400, detail=f"La descripción no puede superar 255 caracteres. Actual: {len(tarea_data.descripcion)}")
        
        # Crear la nueva tarea
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
            "mensaje": "Tarea creada correctamente",
            "id_tarea": nueva_tarea.id_tarea
        }
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
