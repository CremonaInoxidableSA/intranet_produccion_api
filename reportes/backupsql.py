import os
from config.db import SessionLocal
import logging
from dotenv import load_dotenv
import subprocess

logger = logging.getLogger("uvicorn")
load_dotenv()

# Esto capaz que cambia, verificar al migrar al servidor.
mysqldump = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"

def export_database_sql_dump(file_path):
    """
    Genera un archivo .sql con el dump completo de la base de datos MySQL.
    Args:
        file_path: Ruta del archivo .sql a generar
    Returns:
        True si se generó correctamente, False si hay error
    """
    logger.info("Exportando dump de la base de datos MySQL")
    
    try:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")
        
        cmd = [
            mysqldump,
            f"--user={db_user}",
            f"--password={db_password}",
            f"--host={db_host}",
            f"--port={db_port}",
            "--single-transaction",
            "--routines",
            "--triggers",
            db_name
        ]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            logger.error(f"Error en mysqldump: {result.stderr}")
            return False
        
        logger.info(f"Dump de base de datos generado exitosamente en: {file_path}")
        return True
        
    except FileNotFoundError:
        logger.error("mysqldump no está instalado o no está en el PATH")
        return False
    except Exception as e:
        logger.error(f"Error al generar el dump SQL: {str(e)}")
        return False