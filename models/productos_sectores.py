from sqlalchemy import Column, Integer, ForeignKey, PrimaryKeyConstraint
from config.db import Base

class ProductosSectores(Base):
    __tablename__ = "productos_sectores"

    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_sector = Column(Integer, ForeignKey("sectores.id_sector"), nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('id_producto', 'id_sector'),
    )
