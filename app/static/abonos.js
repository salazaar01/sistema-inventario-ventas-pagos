async function cargarClientes() {
    const respuesta = await fetch("/clientes");
    const clientes = await respuesta.json();

    const select = document.getElementById("cliente_id");
    select.innerHTML = '<option value="">Selecciona un cliente</option>';

    clientes.forEach(cliente => {
        const option = document.createElement("option");
        option.value = cliente.id;
        option.textContent = `${cliente.nombre} - ${cliente.numero}`;
        select.appendChild(option);
    });
}

async function cargarSaldo(cliente_id) {
    if (!cliente_id) return;

    const respuesta = await fetch(`/clientes/${cliente_id}/saldo`);
    const data = await respuesta.json();

    document.getElementById("nombre-cliente").textContent = data.cliente_nombre;
    document.getElementById("saldo-cliente").textContent = data.saldo_pendiente;
    document.getElementById("ventas-pendientes").textContent = data.ventas_pendientes;
}

async function cargarDetalleVenta(venta_id) {
    
    const respuesta = await fetch(`/ventas/${venta_id}/chamarras`);
    const chamarras = await respuesta.json();

    const tabla = document.getElementById("tabla-detalle-venta");
    tabla.innerHTML = "";

    chamarras.forEach(chamarra => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${chamarra.codigo}</td>
            <td>${chamarra.descripcion}</td>
            <td>${chamarra.marca}</td>
            <td>${chamarra.color}</td>
            <td>${chamarra.talla}</td>
            <td>$${chamarra.precio_venta}</td>
        `;

        tabla.appendChild(fila);
    });
}

async function cargarVentasCliente(cliente_id) {
    if (!cliente_id) return;

    const respuesta = await fetch(`/clientes/${cliente_id}/ventas`);
    const ventas = await respuesta.json();

    const tabla = document.getElementById("tabla-ventas-cliente");
    tabla.innerHTML = "";

    ventas.forEach(venta => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${venta.venta_id}</td>
            <td>${venta.fecha_venta}</td>
            <td>$${venta.total_bruto}</td>
            <td>$${venta.descuento}</td>
            <td>$${venta.total_final}</td>
            <td>$${venta.pagado}</td>
            <td>$${venta.pendiente}</td>
            <td>${venta.estado}</td>
        `;

        // 👇 Hacer la fila clickeable
        fila.style.cursor = "pointer";

        fila.addEventListener("click", () => {
            cargarDetalleVenta(venta.venta_id);
        });

        tabla.appendChild(fila);
    });
}

async function cargarPagosCliente(cliente_id) {
    if (!cliente_id) return;

    const respuesta = await fetch(`/clientes/${cliente_id}/pagos`);
    const pagos = await respuesta.json();

    const tabla = document.getElementById("tabla-pagos-cliente");
    tabla.innerHTML = "";

    pagos.forEach(pago => {
        const fila = document.createElement("tr");

        fila.innerHTML = `
            <td>${pago.pago_id}</td>
            <td>${pago.fecha_pago}</td>
            <td>$${pago.monto}</td>
        `;

        tabla.appendChild(fila);
    });
}

document.getElementById("cliente_id").addEventListener("change", function () {
    const cliente_id = this.value;
    cargarSaldo(cliente_id);
    cargarVentasCliente(cliente_id);
    cargarPagosCliente(cliente_id);
});

document.getElementById("form-abono").addEventListener("submit", async function (event) {
    event.preventDefault();

    const cliente_id = parseInt(document.getElementById("cliente_id").value);
    const monto = parseFloat(document.getElementById("monto").value);

    const data = {
        cliente_id: cliente_id,
        monto: monto
    };

    const respuesta = await fetch("/abonos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const resultado = await respuesta.json();

    document.getElementById("resultado").textContent =
        `Abono registrado: $${resultado.monto_abonado}`;

    await cargarSaldo(cliente_id);
    await cargarVentasCliente(cliente_id);
    await cargarPagosCliente(cliente_id);

    document.getElementById("monto").value = "";
});



cargarClientes();