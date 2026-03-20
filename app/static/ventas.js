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

document.getElementById("form-venta").addEventListener("submit", async function (event) {
    event.preventDefault();

    const cliente_id = parseInt(document.getElementById("cliente_id").value);
    const codigosTexto = document.getElementById("codigos").value;
    const descuento = parseFloat(document.getElementById("descuento").value || 0);

    const codigos = codigosTexto
        .split(",")
        .map(c => parseInt(c.trim()))
        .filter(c => !isNaN(c));

    const data = {
        cliente_id: cliente_id,
        codigos: codigos,
        descuento: descuento
    };

    const respuesta = await fetch("/ventas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const resultado = await respuesta.json();
    document.getElementById("resultado").textContent = JSON.stringify(resultado, null, 2);
});

cargarClientes();