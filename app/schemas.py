from pydantic import BaseModel


class ChamarraCreate(BaseModel):
    descripcion: str
    marca: str
    color: str
    talla: str
    precio_venta: float

class ClienteCreate(BaseModel):
    nombre: str
    numero: str | None = None
    notas: str | None = None

class VentaCreate(BaseModel):
    cliente_id: int
    codigos: list[int]
    descuento: float = 0

class PagoCreate(BaseModel):
    cliente_id: int
    monto: float