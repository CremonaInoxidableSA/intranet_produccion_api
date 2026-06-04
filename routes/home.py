from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from config.db import SessionLocal
from models.roles import roles

router = APIRouter(prefix="/home", tags=["home"])

class RolRequest(BaseModel):
    rol: str

@router.post("/accesos")
def obtener_accesos(payload: RolRequest):
    db = SessionLocal()
    try:
        registro = db.query(roles).filter(roles.rol == payload.rol).first()
        if not registro:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"accesos": registro.accesos}
    finally:
        db.close()