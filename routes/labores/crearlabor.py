from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from config.db import SessionLocal
from models.labores import Labores
from models.productos_sectores import ProductosSectores
from models.sectores import Sectores
from models.productos import Productos

class CrearLaborRequest(BaseModel):
    nombre: str
    id_sector: int
    id_producto: int 

router = APIRouter(prefix="/labores", tags=["labores"])

@router.post("/crear-labor")
def crear_labor(data: CrearLaborRequest):
    """Crea un nuevo labor.
    Parámetros:
    - nombre: string, nombre del labor
    - id_sector: integer, id del sector
    - id_producto: integer, id del producto
    """
    db = SessionLocal()
    try:
        if not data.nombre or data.nombre.strip() == "":
            return JSONResponse(status_code=400, content={"success": False, "detail": "El nombre del labor no puede estar vacío"})
        
        sector = db.query(Sectores).filter(
            Sectores.id_sector == data.id_sector
        ).first()

        if not sector:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": f"El sector {data.id_sector} no existe"}
            )
        
        producto = db.query(Productos).filter(
            Productos.id_producto == data.id_producto
        ).first()

        if not producto:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": f"El producto {data.id_producto} no existe"}
            )
        
        relacion_valida = db.query(ProductosSectores).filter(
            ProductosSectores.id_producto == data.id_producto,
            ProductosSectores.id_sector == data.id_sector
        ).first()
        
        if not relacion_valida:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": f"El producto {data.id_producto} no está asignado al sector {data.id_sector}"}
            )
        
        # Verificar que no exista ya un labor con el mismo nombre, sector y producto habilitado
        labor_existente = db.query(Labores).filter(
            Labores.nombre == data.nombre.strip(),
            Labores.id_sector == data.id_sector,
            Labores.id_producto == data.id_producto,
            Labores.habilitado == True
        ).first()
        
        if labor_existente:
            return JSONResponse(
                status_code=400,
                content={"success": False, "detail": "Ya existe un labor para este sector y producto con el mismo nombre"}
            )
        
        nuevo_labor = Labores(
            nombre=data.nombre.strip(),
            id_sector=data.id_sector,
            id_producto=data.id_producto,
            habilitado=True
        )
        
        db.add(nuevo_labor)
        db.commit()
        db.refresh(nuevo_labor)
        
        return {
            "id_labor": nuevo_labor.id_labor,
            "success": True,
            "detail": "Labor creado exitosamente"
        }
    
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
    finally:
        db.close()
