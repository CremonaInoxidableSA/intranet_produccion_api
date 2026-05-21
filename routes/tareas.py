from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas

router = APIRouter(prefix="/tareas", tags=["tareas"])


class TareaCreate(BaseModel):
    id_operario: int
    sector: Optional[str] = None  # informativo, no se persiste en tareas
    numero_op: int
    numero_plano: int
    labor: str
    fecha_inicio: datetime
    fecha_fin: datetime
    duracion_tarea: int


@router.put("/cargar-tarea")
def cargar_tarea(tarea: TareaCreate):
    """Guarda una nueva tarea en base de datos."""
    db = SessionLocal()
    try:
        nueva = Tareas(
            id_operario=tarea.id_operario,
            numero_op=tarea.numero_op,
            numero_plano=tarea.numero_plano,
            labor=tarea.labor,
            fecha_inicio=tarea.fecha_inicio,
            fecha_fin=tarea.fecha_fin,
            duracion_tarea=tarea.duracion_tarea,
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return {
            "mensaje": "Tarea creada correctamente",
            "id_tarea": nueva.id_tarea,
            "id_operario": nueva.id_operario,
            "numero_op": nueva.numero_op,
            "numero_plano": nueva.numero_plano,
            "labor": nueva.labor,
            "fecha_inicio": nueva.fecha_inicio,
            "fecha_fin": nueva.fecha_fin,
            "duracion_tarea": nueva.duracion_tarea,
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
