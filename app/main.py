from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models, schemas
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request


app = FastAPI(title="Sistema de Chamarras")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/inventario", response_class=HTMLResponse)
def pagina_inventario(request: Request):
    return templates.TemplateResponse("inventario.html", {"request": request})

@app.get("/ventas-ui", response_class=HTMLResponse)
def pagina_ventas(request: Request):
    return templates.TemplateResponse("ventas.html", {"request": request})

@app.get("/abonos-ui", response_class=HTMLResponse)
def pagina_abonos(request: Request):
    return templates.TemplateResponse("abonos.html", {"request": request})

@app.get("/")
def inicio():
    return {"mensaje": "Sistema de chamarras funcionando correctamente"}

@app.post("/chamarras")
def crear_chamarra(chamarra: schemas.ChamarraCreate, db: Session = Depends(get_db)):
    ultima_chamarra = db.query(models.Chamarra).order_by(models.Chamarra.codigo.desc()).first()

    if ultima_chamarra:
        siguiente_codigo = ultima_chamarra.codigo + 1
    else:
        siguiente_codigo = 1

    nueva_chamarra = models.Chamarra(
        codigo=siguiente_codigo,
        descripcion=chamarra.descripcion,
        marca=chamarra.marca,
        color=chamarra.color,
        talla=chamarra.talla,
        precio_venta=chamarra.precio_venta,
        estado="disponible"
    )

    db.add(nueva_chamarra)
    db.commit()
    db.refresh(nueva_chamarra)

    return {
        "mensaje": "Chamarra creada correctamente",
        "id": nueva_chamarra.id,
        "codigo": nueva_chamarra.codigo
    }

@app.get("/chamarras")
def listar_chamarras(db: Session = Depends(get_db)):
    chamarras = db.query(models.Chamarra).all()
    return chamarras

@app.get("/chamarras/{codigo}")
def obtener_chamarra(codigo: int, db: Session = Depends(get_db)):
    chamarra = db.query(models.Chamarra).filter(models.Chamarra.codigo == codigo).first()

    if not chamarra:
        return {"error": "Chamarra no encontrada"}

    return chamarra



@app.post("/clientes")
def crear_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    nuevo_cliente = models.Cliente(
        nombre=cliente.nombre,
        numero=cliente.numero,
        notas=cliente.notas
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return {
        "mensaje": "Cliente creado correctamente",
        "id": nuevo_cliente.id,
        "nombre": nuevo_cliente.nombre
    }

@app.get("/clientes")
def listar_clientes(db: Session = Depends(get_db)):
    clientes = db.query(models.Cliente).all()
    return clientes



@app.post("/ventas")
def crear_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == venta.cliente_id).first()

    if not cliente:
        return {"error": "Cliente no encontrado"}

    chamarras = db.query(models.Chamarra).filter(models.Chamarra.codigo.in_(venta.codigos)).all()

    if len(chamarras) != len(venta.codigos):
        return {"error": "Una o más chamarras no existen"}

    for chamarra in chamarras:
        if chamarra.estado != "disponible":
            return {"error": f"La chamarra con código {chamarra.codigo} no está disponible"}

    total_bruto = sum(chamarra.precio_venta for chamarra in chamarras)
    total_final = total_bruto - venta.descuento

    nueva_venta = models.Venta(
        cliente_id=venta.cliente_id,
        total_bruto=total_bruto,
        descuento=venta.descuento,
        total_final=total_final,
        estado="pendiente"
    )

    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    for chamarra in chamarras:
        detalle = models.DetalleVenta(
            venta_id=nueva_venta.id,
            chamarra_id=chamarra.id
        )
        db.add(detalle)
        chamarra.estado = "vendida"

    db.commit()

    return {
        "mensaje": "Venta creada correctamente",
        "venta_id": nueva_venta.id,
        "total_bruto": total_bruto,
        "descuento": venta.descuento,
        "total_final": total_final
    }


@app.post("/abonos")
def registrar_abono(pago: schemas.PagoCreate, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == pago.cliente_id).first()

    if not cliente:
        return {"error": "Cliente no encontrado"}

    nuevo_pago = models.Pago(
        cliente_id=pago.cliente_id,
        monto=pago.monto
    )

    db.add(nuevo_pago)

    ventas_pendientes = (
        db.query(models.Venta)
        .filter(
            models.Venta.cliente_id == pago.cliente_id,
            models.Venta.estado == "pendiente"
        )
        .order_by(models.Venta.id.asc())
        .all()
    )

    monto_restante = pago.monto

    for venta in ventas_pendientes:
        saldo_venta = venta.total_final - venta.monto_pagado

        if monto_restante <= 0:
            break

        if monto_restante >= saldo_venta:
            venta.monto_pagado += saldo_venta
            venta.estado = "pagada"
            monto_restante -= saldo_venta
        else:
            venta.monto_pagado += monto_restante
            monto_restante = 0

    db.commit()

    return {
        "mensaje": "Abono registrado correctamente",
        "cliente_id": pago.cliente_id,
        "monto_abonado": pago.monto,
        "monto_sin_aplicar": monto_restante
    }


@app.get("/clientes/{cliente_id}/ventas")
def obtener_ventas_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    if not cliente:
        return {"error": "Cliente no encontrado"}

    ventas = db.query(models.Venta).filter(models.Venta.cliente_id == cliente_id).all()

    resultado = []

    for venta in ventas:
        pendiente = venta.total_final - venta.monto_pagado

        resultado.append({
            "venta_id": venta.id,
            "fecha_venta": venta.fecha_venta.strftime("%Y-%m-%d %H:%M"),
            "total_bruto": venta.total_bruto,
            "descuento": venta.descuento,
            "total_final": venta.total_final,
            "pagado": venta.monto_pagado,
            "pendiente": pendiente,
            "estado": venta.estado
        })

    return resultado

@app.get("/clientes/{cliente_id}/pagos")
def obtener_pagos_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    if not cliente:
        return {"error": "Cliente no encontrado"}

    pagos = (
        db.query(models.Pago)
        .filter(models.Pago.cliente_id == cliente_id)
        .order_by(models.Pago.fecha_pago.asc())
        .all()
    )

    resultado = []

    for pago in pagos:
        resultado.append({
            "pago_id": pago.id,
            "fecha_pago": pago.fecha_pago.strftime("%Y-%m-%d %H:%M"),
            "monto": pago.monto
        })

    return resultado

@app.get("/clientes/{cliente_id}/saldo")
def obtener_saldo_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

    if not cliente:
        return {"error": "Cliente no encontrado"}

    ventas_pendientes = (
        db.query(models.Venta)
        .filter(
            models.Venta.cliente_id == cliente_id,
            models.Venta.estado == "pendiente"
        )
        .all()
    )

    saldo_total = sum(venta.total_final - venta.monto_pagado for venta in ventas_pendientes)

    return {
        "cliente_id": cliente_id,
        "cliente_nombre": cliente.nombre,
        "saldo_pendiente": saldo_total,
        "ventas_pendientes": len(ventas_pendientes)
    }


@app.get("/ventas")
def listar_ventas(db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).all()
    return ventas

@app.get("/ventas/{venta_id}/chamarras")
def obtener_chamarras_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id == venta_id).first()

    if not venta:
        return {"error": "Venta no encontrada"}

    detalles = (
        db.query(models.DetalleVenta, models.Chamarra)
        .join(models.Chamarra, models.DetalleVenta.chamarra_id == models.Chamarra.id)
        .filter(models.DetalleVenta.venta_id == venta_id)
        .all()
    )

    resultado = []

    for _, chamarra in detalles:
        resultado.append({
            "codigo": chamarra.codigo,
            "descripcion": chamarra.descripcion,
            "marca": chamarra.marca,
            "color": chamarra.color,
            "talla": chamarra.talla,
            "precio_venta": chamarra.precio_venta
        })

    return resultado