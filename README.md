# 🧥 Sistema de Inventario y Ventas de Chamarras

Aplicación web para la gestión de inventario, ventas y pagos (abonos) enfocada en pequeños negocios de retail.

Este sistema permite controlar productos, registrar ventas a crédito y dar seguimiento a los pagos de los clientes de manera sencilla y eficiente.

---

## 🚀 Funcionalidades principales

- 📦 Gestión de inventario de chamarras
  - Alta de productos
  - Control de estado (disponible / vendida)

- 💸 Registro de ventas
  - Asociación de múltiples productos a una venta
  - Aplicación de descuentos
  - Cálculo automático de totales

- 👤 Gestión de clientes
  - Registro de clientes
  - Relación con ventas y pagos

- 💵 Sistema de abonos (pagos)
  - Registro de pagos por cliente
  - Aplicación automática a ventas pendientes
  - Actualización de estado (pendiente / pagada)

- 📊 Seguimiento financiero
  - Historial de ventas por cliente
  - Historial de pagos
  - Cálculo de saldo pendiente

---

## 🧱 Tecnologías utilizadas

- **Backend:** FastAPI
- **Base de datos:** SQLite + SQLAlchemy
- **Frontend:** HTML + CSS + JavaScript (Vanilla)
- **Templates:** Jinja2

---

## 🧠 Arquitectura

El proyecto sigue una estructura modular:

```

app/
├── models.py       # Modelos de base de datos
├── schemas.py      # Esquemas (Pydantic)
├── database.py     # Configuración de DB
├── templates/      # HTML (Jinja2)
├── static/         # JS y CSS
└── main.py         # API y rutas

```

Separación clara entre:
- lógica de negocio (backend)
- presentación (templates)
- interacción (JavaScript)

---

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/salazaar01/sistema-inventario-ventas-pagos.git
cd sistema-inventario-ventas-pagos
````

2. Crear entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar el servidor:

```bash
uvicorn app.main:app --reload
```

5. Abrir en navegador:

* Inventario: [http://127.0.0.1:8000/inventario](http://127.0.0.1:8000/inventario)
* Ventas: [http://127.0.0.1:8000/ventas-ui](http://127.0.0.1:8000/ventas-ui)
* Abonos: [http://127.0.0.1:8000/abonos-ui](http://127.0.0.1:8000/abonos-ui)

---

## 🔄 Lógica de negocio destacada

* Aplicación automática de pagos a ventas pendientes en orden cronológico
* Cálculo dinámico de saldo por cliente
* Control de estado de productos en inventario tras una venta

---

## 🎯 Objetivo del proyecto

Este sistema fue desarrollado para reemplazar procesos manuales (Excel + registros físicos) por una solución digital estructurada, mejorando:

* control financiero
* trazabilidad de ventas
* eficiencia operativa

---

## 📌 Posibles mejoras futuras

* Dashboard con métricas clave
* Autenticación de usuarios
* Deploy en la nube (Render / Railway)
* Exportación de reportes (PDF / Excel)
* Interfaz más avanzada (React)

---

## 👨‍💻 Autor

**Diego Salazar Barrera**
Ingeniería Mecatrónica – UNAM
Interesado en robótica, software y sistemas inteligentes
