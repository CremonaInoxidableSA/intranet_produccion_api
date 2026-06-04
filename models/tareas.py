from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from config.db import Base

class Tareas(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    id_operario = Column(Integer, ForeignKey("operarios.id_operario"), nullable=True)
    numero_op = Column(Integer, nullable=True)
    numero_plano = Column(Integer, nullable=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=True)
    id_labor = Column(Integer, ForeignKey("labores.id_labor"), nullable=True)
    descripcion= Column(String(255), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    duracion_tarea = Column(Integer, nullable=True)
    pausas_reanudaciones = Column(JSON, nullable=True)
