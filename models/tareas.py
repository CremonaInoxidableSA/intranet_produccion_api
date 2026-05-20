from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base

class Tareas(Base):
    __tablename__ = "tareas"

    id_tarea = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(Integer, ForeignKey("operarios.id_operario"), nullable=True)
    usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    numero_op = Column(Integer, nullable=True)
    numero_plano = Column(Integer, nullable=True)
    labor = Column(String(200), nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    duracion_tarea = Column(Integer, nullable=True)
