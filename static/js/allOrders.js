async function dateFilter(){
    let dateTag = document.getElementById("filtroFecha").value
    console.log(dateTag)
    let [año, mes, dia]  = dateTag.split("-")
    
    console.log(dia)

    let btnFiltrar = await document.getElementById("anclaFiltrarDia")
    btnFiltrar.href= `http://127.0.0.1:8000/showAllOrdersDay/${dia}`
    console.log(btnFiltrar.href)
} 
