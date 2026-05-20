from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.db import Base

class Operarios(Base):
    __tablename__ = "operarios"

    id_operario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=True)
    legajo = Column(String(100), nullable=True)
    sector = Column(String(100), nullable=True)