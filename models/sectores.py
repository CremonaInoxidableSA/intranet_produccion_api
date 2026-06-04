from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.db import Base

class Sectores(Base):
    __tablename__ = "sectores"

    id_sector = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)