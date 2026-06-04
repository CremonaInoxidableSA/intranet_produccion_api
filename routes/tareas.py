from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from config.db import SessionLocal
from sqlalchemy import func, or_
from models.tareas import Tareas
from models.operarios import Operarios
from models.labores import Labores
from models.usuarios import Usuarios

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


@router.get("/comprobacion")
def comprobacion(nombre: str, legajo: int):
    """Verifica si existe una tarea sin `fecha_fin` para el operario identificado por `nombre` y `legajo`."""
    db = SessionLocal()
    try:
        oper = db.query(Operarios).filter(Operarios.nombre == nombre, Operarios.legajo == legajo).first()
        if not oper:
            return {"existe": False, "message": "Operario no encontrado"}

        # Buscar tarea sin fecha_fin y que esté activa (no pausada)
        # Activa si:
        # - `pausas_reanudaciones` es NULL, o
        # - tiene longitud 0, o
        # - su longitud es impar (última posición es índice impar => última acción fue reanudación)
        tarea = (
            db.query(Tareas)
            .filter(
                Tareas.id_operario == oper.id_operario,
                Tareas.fecha_fin.is_(None),
                or_(
                    Tareas.pausas_reanudaciones == None,
                    func.JSON_LENGTH(Tareas.pausas_reanudaciones) == 0,
                    func.mod(func.JSON_LENGTH(Tareas.pausas_reanudaciones), 2) == 0,
                ),
            )
            .first()
        )
        if tarea:
            labor = None
            if getattr(tarea, 'id_labor', None) is not None:
                labor = db.query(Labores).filter(Labores.id_labor == tarea.id_labor).first()

            usuario = None
            if getattr(tarea, 'id_usuario', None) is not None:
                usuario = db.query(Usuarios).filter(Usuarios.id == tarea.id_usuario).first()

            creador = None
            if usuario:
                apellido = usuario.apellido or ""
                nombre_usuario = usuario.nombre or ""
                full = f"{apellido} {nombre_usuario}".strip()
                creador = full if full else None

            return {
                "existe": True,
                "id_tarea": tarea.id_tarea,
                "nombre.creador": creador,
                "nombre.labor": labor.nombre if labor else None,
            }

        return {"existe": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()