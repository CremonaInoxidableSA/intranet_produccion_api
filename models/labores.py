from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base

class Labores(Base):
    __tablename__ = "labores"

    id_labor = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_sector = Column(Integer, ForeignKey("sectores.id_sector"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    nombre = Column(String(255), nullable=False)