from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
import tempfile
from reportes.backupmaster import export_todas_tareas_finalizadas_to_excel
from reportes.backupsql import export_database_sql_dump
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/backups", tags=["backups"])

@router.get("/descargar-excel-master")
def descargar_backup_excel_master():
    """
    Descarga el reporte Excel de todas las tareas finalizadas.
    
    Returns:
        Archivo Excel con el reporte master de tareas
    """
    try:
        temp_dir = tempfile.gettempdir()
        archivo_excel = os.path.join(temp_dir, "reporte_master_tareas.xlsx")
        
        resultado = export_todas_tareas_finalizadas_to_excel(archivo_excel)
        
        if not resultado:
            return JSONResponse(status_code=404, content={"success": False, "detail": "No se encontraron datos para el reporte master"})
        
        if not os.path.exists(archivo_excel):
            return JSONResponse(status_code=500, content={"success": False, "detail": f"Error al generar el archivo Excel"})
        
        return FileResponse(
            path=archivo_excel,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="reporte_master_tareas.xlsx"
        )
        
    except HTTPException as e:
        logger.error(f"Error HTTP al descargar reporte master: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al descargar reporte master: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/descargar-dump-sql")
def descargar_dump_sql():
    """
    Descarga el dump SQL completo de la base de datos.
    
    Returns:
        Archivo .sql con el backup de la base de datos
    """
    try:
        temp_dir = tempfile.gettempdir()
        archivo_sql = os.path.join(temp_dir, "backup_base_datos.sql")
        
        resultado = export_database_sql_dump(archivo_sql)
        
        if not resultado:
            return JSONResponse(status_code=500, content={"success": False, "detail": "Error al generar el dump SQL"})
        
        if not os.path.exists(archivo_sql):
            return JSONResponse(status_code=500, content={"success": False, "detail": "Error al generar el archivo SQL"})
        
        return FileResponse(
            path=archivo_sql,
            media_type="text/plain",
            filename="backup_base_datos.sql"
        )
        
    except HTTPException as e:
        logger.error(f"Error HTTP al descargar dump SQL: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al descargar dump SQL: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )