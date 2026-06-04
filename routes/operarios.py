from fastapi import APIRouter, HTTPException
from config.db import SessionLocal
from models.operarios import Operarios
from models.sectores import Sectores
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


@router.get("/lista-operarios-habilitados")
def get_operarios():
    """Obtiene el listado de todos los operarios habilitados."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Operarios, Sectores.nombre)
            .outerjoin(Sectores, Operarios.id_sector == Sectores.id_sector)
            .filter(Operarios.habilitado == True)
            .all()
        )
        return [
            {
                "nombre": o.nombre,
                "legajo": o.legajo,
                "sector": sector_nombre
            }
            for o, sector_nombre in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()

@router.get("/lista-operarios-total")
def get_operarios_total():
    """Obtiene el listado de todos los operarios, sin importar si están habilitados o no."""
    db = SessionLocal()
    try:
        rows = (
            db.query(Operarios, Sectores.nombre)
            .outerjoin(Sectores, Operarios.id_sector == Sectores.id_sector)
            .all()
        )
        return [
            {
                "nombre": o.nombre,
                "legajo": o.legajo,
                "sector": sector_nombre
            }
            for o, sector_nombre in rows
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
