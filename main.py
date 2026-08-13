from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

from config import db
from config.sql_loader import cargar_datos_iniciales

from routers.sectores import router as sector_router

from routers.comprobaciones import router as comprobaciones_router

from routers.tareas.pausarreanudar import router as pausarreanudar_router
from routers.tareas.eliminar import router as eliminar_router
from routers.tareas.listadotareaspersonal import router as listadotareaspersonal_router
from routers.tareas.datosfiltrosencurso import router as datosfiltrosencurso_router
from routers.tareas.datosfiltrosfinalizadas import router as datosfiltrosfinalizadas_router
from routers.tareas.tareasactivasgeneral import router as tareasactivasgeneral_router
from routers.tareas.tareasfinalizadasgeneral import router as tareasfinalizadasgeneral_router
from routers.tareas.detalletareaactiva import router as detalletareaactiva_router
from routers.tareas.detalletareafinalizada import router as detalletareafinalizada_router
from routers.tareas.reiniciartiempo import router as reiniciartiempo_router
from routers.tareas.finalizartarea import router as finalizartarea_router
from routers.tareas.guardacambios import router as guardacambios_router
from routers.tareas.creartarea import router as creartarea_router

from routers.productos.actualizarproductos import router as actualizarproductos_router
from routers.productos.listaproductos import router as listaproductos_router
from routers.productos.eliminarproductos import router as eliminarproductos_router
from routers.productos.crearproducto import router as crearproducto_router

from routers.labores.listalabores import router as labores_router
from routers.labores.crearlabor import router as crearlabor_router
from routers.labores.eliminarlabor import router as eliminarlabor_router

from routers.reportes.descargarreportes import router as descargarreportes_router

from routers.backups.descargarbackups import router as descargarbackups_router

from models.tareas import Tareas
from models.labores import Labores
from models.productos import Productos
from models.sectores import Sectores
from models.productos_sectores import ProductosSectores

from monitor.monitor_automatico import iniciar_monitor_pausas, detener_monitor_pausas

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sector_router)
app.include_router(actualizarproductos_router)
app.include_router(listaproductos_router)
app.include_router(eliminarproductos_router)
app.include_router(crearproducto_router)
app.include_router(labores_router)
app.include_router(crearlabor_router)
app.include_router(eliminarlabor_router)
app.include_router(descargarreportes_router)
app.include_router(pausarreanudar_router)
app.include_router(eliminar_router)
app.include_router(creartarea_router)
app.include_router(detalletareaactiva_router)
app.include_router(detalletareafinalizada_router)
app.include_router(datosfiltrosencurso_router)
app.include_router(datosfiltrosfinalizadas_router)
app.include_router(tareasactivasgeneral_router)
app.include_router(tareasfinalizadasgeneral_router)
app.include_router(reiniciartiempo_router)
app.include_router(finalizartarea_router)
app.include_router(guardacambios_router)
app.include_router(listadotareaspersonal_router)
app.include_router(comprobaciones_router)
app.include_router(descargarbackups_router)


@app.on_event("startup")
def startup_event():
    iniciar_monitor_pausas()


@app.on_event("shutdown")
def shutdown_event():
    detener_monitor_pausas()