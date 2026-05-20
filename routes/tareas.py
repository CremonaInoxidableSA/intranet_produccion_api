from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
from models.tareas import Tareas
from models.usuarios import Usuarios

router = APIRouter(prefix="/tareas", tags=["tareas"])


def get_db():
    """Obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_tareas():
    """Obtiene todas las tareas registradas."""
    db = SessionLocal()
    try:
        tareas = db.query(Tareas).all()
        return [
            {
                "id_tarea": t.id_tarea,
                "titulo": t.titulo,
                "descripcion": t.descripcion,
                "estado": t.estado,
                "prioridad": t.prioridad,
                "completada": t.completada,
                "fecha_creacion": t.fecha_creacion.isoformat() if t.fecha_creacion else None,
                "fecha_vencimiento": t.fecha_vencimiento.isoformat() if t.fecha_vencimiento else None,
                "id_usuario": t.id_usuario,
            }
            for t in tareas
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()


@router.get("/{id_tarea}")
def get_tarea(id_tarea: int):
    """Obtiene el detalle de una tarea por su ID."""
    db = SessionLocal()
    try:
        tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return {
            "id_tarea": tarea.id_tarea,
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "estado": tarea.estado,
            "prioridad": tarea.prioridad,
            "completada": tarea.completada,
            "fecha_creacion": tarea.fecha_creacion.isoformat() if tarea.fecha_creacion else None,
            "fecha_vencimiento": tarea.fecha_vencimiento.isoformat() if tarea.fecha_vencimiento else None,
            "id_usuario": tarea.id_usuario,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()


@router.get("/por_usuario/{id_usuario}")
def get_tareas_por_usuario(id_usuario: int):
    """Obtiene todas las tareas asignadas a un usuario."""
    db = SessionLocal()
    try:
        usuario = db.query(Usuarios).filter(Usuarios.id == id_usuario).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        tareas = db.query(Tareas).filter(Tareas.id_usuario == id_usuario).all()
        return [
            {
                "id_tarea": t.id_tarea,
                "titulo": t.titulo,
                "descripcion": t.descripcion,
                "estado": t.estado,
                "prioridad": t.prioridad,
                "completada": t.completada,
                "fecha_creacion": t.fecha_creacion.isoformat() if t.fecha_creacion else None,
                "fecha_vencimiento": t.fecha_vencimiento.isoformat() if t.fecha_vencimiento else None,
            }
            for t in tareas
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
