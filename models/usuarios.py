from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from config.db import Base

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    usuario = Column(String(100), nullable=True)
    nombre = Column(String(100), nullable=True)
    apellido = Column(String(100), nullable=True)
    rol = Column(String(100), ForeignKey("roles.rol"), nullable=True)
    password_hash = Column(String(255), nullable=True)
    habilitado = Column(Boolean, default=True)