from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.db import Base

class Productos(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)