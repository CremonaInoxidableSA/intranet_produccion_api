from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from config.db import Base

class roles(Base):
    __tablename__ = "roles"

    rol = Column(String(100), primary_key=True, index=True, nullable=False)
    accesos = Column(JSON, nullable=True)