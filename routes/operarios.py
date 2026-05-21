from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.operarios import Operarios
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/operarios", tags=["operarios"])


class OperarioUpdate(BaseModel):
    id_operario: int
    nombre: Optional[str] = None
    legajo: Optional[str] = None
    sector: Optional[str] = None
    habilitado: Optional[bool] = None


class OperarioCreate(BaseModel):
    nombre: str
    legajo: str
    sector: str


@router.get("")
def get_operarios():
    """Obtiene el listado de todos los operarios."""
    db = SessionLocal()
    try:
        operarios = db.query(Operarios).all()
        return [
            {
                "id_operario": o.id_operario,
                "nombre": o.nombre,
                "legajo": o.legajo,
                "sector": o.sector,
                "habilitado": o.habilitado,
            }
            for o in operarios
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()


@router.put("/editar-operario")
def editar_operario(operarios: List[OperarioUpdate]):
    """Edita uno o varios operarios recibidos desde el front."""
    db = SessionLocal()
    try:
        actualizados = []
        for item in operarios:
            operario = db.query(Operarios).filter(Operarios.id_operario == item.id_operario).first()
            if not operario:
                raise HTTPException(status_code=404, detail=f"Operario con id {item.id_operario} no encontrado")
            if item.nombre is not None:
                operario.nombre = item.nombre
            if item.legajo is not None:
                operario.legajo = item.legajo
            if item.sector is not None:
                operario.sector = item.sector
            if item.habilitado is not None:
                operario.habilitado = item.habilitado
            actualizados.append(item.id_operario)
        db.commit()
        return {"mensaje": "Operarios actualizados correctamente", "ids_actualizados": actualizados}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()


@router.put("/cargar-operario")
def cargar_operario(operario: OperarioCreate):
    """Crea un nuevo operario con ID autogenerado y habilitado en True por defecto."""
    db = SessionLocal()
    try:
        nuevo = Operarios(
            nombre=operario.nombre,
            legajo=operario.legajo,
            sector=operario.sector,
            habilitado=True,
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {
            "mensaje": "Operario creado correctamente",
            "id_operario": nuevo.id_operario,
            "nombre": nuevo.nombre,
            "legajo": nuevo.legajo,
            "sector": nuevo.sector,
            "habilitado": nuevo.habilitado,
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
