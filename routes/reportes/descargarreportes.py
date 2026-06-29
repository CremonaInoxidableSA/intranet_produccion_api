from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import tempfile
from reportes.reportetarea import export_tarea_individual_to_excel
from reportes.reporteporfecha import export_tareas_por_fecha_to_excel
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

@router.get("/descargar-reporte-fecha")
def descargar_reporte_tarea_fecha(fecha_inicio_filtrado: str, fecha_fin_filtrado: str):
    """
    Descarga el reporte Excel de todas las tareas en un rango de fechas.
    
    Args:
        fecha_inicio_filtrado: Fecha de inicio en formato YYYY-MM-DD
        fecha_fin_filtrado: Fecha de fin en formato YYYY-MM-DD
    
    Returns:
        Archivo Excel con el reporte de tareas
    """
    try:
        temp_dir = tempfile.gettempdir()
        archivo_excel = os.path.join(temp_dir, f"tareas_{fecha_inicio_filtrado}_{fecha_fin_filtrado}_reporte.xlsx")
        
        resultado = export_tareas_por_fecha_to_excel(archivo_excel, fecha_inicio_filtrado, fecha_fin_filtrado)
        
        if not resultado:
            raise JSONResponse(status_code=404, content={"success": False, "detail": f"No se encontraron datos para el rango de fechas: {fecha_inicio_filtrado} a {fecha_fin_filtrado}"})
        
        if not os.path.exists(archivo_excel):
            raise JSONResponse(status_code=500, content={"success": False, "detail": f"Error al generar el archivo Excel"})
        
        return FileResponse(
            path=archivo_excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"tareas_{fecha_inicio_filtrado}_{fecha_fin_filtrado}_reporte.xlsx"
        )
        
    except HTTPException as e:
        logger.error(f"Error HTTP al descargar reporte de fechas {fecha_inicio_filtrado} a {fecha_fin_filtrado}: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al descargar reporte de fechas {fecha_inicio_filtrado} a {fecha_fin_filtrado}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
