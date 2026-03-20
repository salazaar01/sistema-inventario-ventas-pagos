async function cargarChamarras() {
    const respuesta = await fetch("/chamarras");
    const chamarras = await respuesta.json();

    const tabla = document.getElementById("tabla-chamarras");
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
            <td>${chamarra.estado}</td>
        `;

        tabla.appendChild(fila);
    });
}


document.getElementById("form-chamarra").addEventListener("submit", async function (event) {
    event.preventDefault();

    const nuevaChamarra = {
        descripcion: document.getElementById("descripcion").value,
        marca: document.getElementById("marca").value,
        color: document.getElementById("color").value,
        talla: document.getElementById("talla").value,
        precio_venta: parseFloat(document.getElementById("precio_venta").value)
    };

    const respuesta = await fetch("/chamarras", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(nuevaChamarra)
    });

    if (respuesta.ok) {
        document.getElementById("form-chamarra").reset();
        cargarChamarras();
    } else {
        alert("Error al agregar la chamarra");
    }
});


cargarChamarras();