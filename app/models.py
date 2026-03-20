from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.database import Base
from datetime import datetime

class Chamarra(Base):
    __tablename__ = "chamarras"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, unique=True, nullable=False)
    descripcion = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    color = Column(String, nullable=False)
    talla = Column(String, nullable=False)
    precio_venta = Column(Float, nullable=False)
    estado = Column(String, nullable=False, default="disponible")


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    numero = Column(String, nullable=False)
    notas = Column(String, nullable=True)



class Venta(Base): 
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer,ForeignKey("clientes.id"), nullable=False)
    total_bruto = Column(Float, nullable=False)
    descuento = Column(Float, nullable=False, default=0)
    total_final = Column(Float, nullable=False)
    monto_pagado = Column(Float, nullable=False, default=0)
    estado = Column(String, nullable=False, default="pendiente")
    fecha_venta = Column(DateTime, nullable=False, default=datetime.now)


class DetalleVenta(Base):
    __tablename__ = "detalle_venta"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)
    chamarra_id = Column(Integer, ForeignKey("chamarras.id"), nullable=False)



class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(DateTime, nullable=False, default=datetime.now)