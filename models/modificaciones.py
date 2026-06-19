from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
from config.db import Base

class Modificaciones(Base):
    __tablename__ = "modificaciones"

    id_modificacion = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario_logeado = Column(String(255), nullable=True)
    id_tarea = Column(Integer, ForeignKey("tareas.id_tarea"), nullable=False)
    descripcion = Column(String(255), nullable=True)