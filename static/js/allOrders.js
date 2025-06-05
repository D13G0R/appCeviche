async function dateFilter() {
    let dateTag = document.getElementById("filtroFecha").value; // "YYYY-MM-DD"
    console.log(dateTag);

    // Asumimos que tienes un enlace o botón
    let btnFiltrar = await document.getElementById("anclaFiltrarDia");
    // La URL ahora lleva la fecha completa
    btnFiltrar.href = `http://127.0.0.1:8000/showAllOrdersDay/${dateTag}`;
    console.log(btnFiltrar.href);
}