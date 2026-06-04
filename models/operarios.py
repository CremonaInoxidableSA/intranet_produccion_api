from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base

class Operarios(Base):
    __tablename__ = "operarios"

    id_operario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=True)
    legajo = Column(Integer, nullable=True)
    id_sector = Column(Integer, ForeignKey("sectores.id_sector"), nullable=True)
    habilitado = Column(Boolean, default=True)