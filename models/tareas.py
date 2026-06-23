from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from config.db import Base

class Tareas(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario_logeado = Column(Integer, nullable=False)
    nombre_usuario_logeado = Column(String(100), nullable=False)
    apellido_usuario_logeado = Column(String(100), nullable=False)
    id_operario_seleccionado = Column(Integer, nullable=False)
    nombre_operario_seleccionado = Column(String(100), nullable=False)
    apellido_operario_seleccionado = Column(String(100), nullable=False)
    numero_op = Column(Integer, nullable=False)
    numero_plano = Column(Integer, nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_labor = Column(Integer, ForeignKey("labores.id_labor"), nullable=False)
    descripcion= Column(String(255), nullable=True)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True)
    tiempo_extra = Column(Integer, nullable=True)
    duracion_tarea = Column(Integer, nullable=True)
    pausas_reanudaciones = Column(JSON, nullable=True)
