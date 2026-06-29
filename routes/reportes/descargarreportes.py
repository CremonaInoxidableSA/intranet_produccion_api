from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import tempfile
from reportes.reportetarea import export_tarea_individual_to_excel
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/reportes", tags=["reportes"])

@router.get("/descargar-reporte-tarea")
def descargar_reporte_tarea_individual(id_tarea: int):
    """
    Descarga el reporte Excel de una tarea individual específica.
    
    Args:
        id_tarea: ID de la tarea a reportar
    
    Returns:
        Archivo Excel con el reporte de la tarea
    """
    try:
        temp_dir = tempfile.gettempdir()
        archivo_excel = os.path.join(temp_dir, f"tarea_{id_tarea}_reporte.xlsx")
        
        resultado = export_tarea_individual_to_excel(archivo_excel, id_tarea)
        
        if not resultado:
            raise JSONResponse(status_code=404, content={"success": False, "detail": f"No se encontraron datos para la tarea ID: {id_tarea}"})
        
        if not os.path.exists(archivo_excel):
            raise JSONResponse(status_code=500, content={"success": False, "detail": f"Error al generar el archivo Excel"})
        
        return FileResponse(
            path=archivo_excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"tarea_{id_tarea}_reporte.xlsx"
        )
        
    except HTTPException as e:
        logger.error(f"Error HTTP al descargar reporte de tarea {id_tarea}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al descargar reporte de tarea {id_tarea}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
