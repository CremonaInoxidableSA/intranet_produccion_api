from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base

class Labores(Base):
    __tablename__ = "labores"

    id_labor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sector = Column(Integer, ForeignKey("sectores.id_sector"), nullable=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=True)
    nombre = Column(String(100), nullable=False)