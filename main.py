from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

from config import db
from config.sql_loader import cargar_datos_iniciales

from routes.sectores import router as sector_router
from routes.productos import router as productos_router
from routes.labores import router as labores_router

from routes.comprobaciones import router as comprobaciones_router

from routes.tareas.pausarreanudar import router as pausarreanudar_router
from routes.tareas.eliminar import router as eliminar_router
from routes.tareas.listadotareaspersonal import router as listadotareaspersonal_router
from routes.tareas.detalletareaactiva import router as detalletareaactiva_router
from routes.tareas.reiniciartiempo import router as reiniciartiempo_router
from routes.tareas.finalizartarea import router as finalizartarea_router
from routes.tareas.guardacambios import router as guardacambios_router

from models.tareas import Tareas
from models.labores import Labores
from models.productos import Productos
from models.sectores import Sectores
from models.productos_sectores import ProductosSectores

load_dotenv()

with create_engine(
    f"mysql+pymysql://{os.getenv('DB_USER')}:{quote_plus(os.getenv('DB_PASSWORD', ''))}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
).connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}"))
    print(f"✓ Base de datos '{os.getenv('DB_NAME')}' verificada o creada exitosamente")

db.Base.metadata.drop_all(bind=db.engine)
db.Base.metadata.create_all(bind=db.engine)
cargar_datos_iniciales()

app = FastAPI(title="API cr_produccion", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"http://{os.getenv('FRONTEND_IP')}:3000",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sector_router)
app.include_router(productos_router)
app.include_router(labores_router)
app.include_router(pausarreanudar_router)
app.include_router(eliminar_router)
app.include_router(detalletareaactiva_router)
app.include_router(reiniciartiempo_router)
app.include_router(finalizartarea_router)
app.include_router(guardacambios_router)
app.include_router(listadotareaspersonal_router)
app.include_router(comprobaciones_router)