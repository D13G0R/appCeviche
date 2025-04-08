pedidoJson = []

function addToPanel(type, id, name, description, price = null) {

    const panelList = document.getElementById('panel-list');
    const listItem = document.createElement('li');

    listItem.className = "bg-white p-2 rounded-lg shadow-md mb-2";
    listItem.innerHTML = `
                            <h3 class="font-semibold">${type} <br/> ${name}</h3>  

                            <p class="text-sm">${description}.</p>                
                            
                            <div class ="rounded-lg bg-blue-200 mt-2">
                                <div class= 'w-full flex rounded-lg'>
                                    <p class = "font-bold ">Precio:</p>
                                    ${price ? `<p class ="pl-4">$${price}</p>` : ''} 
                                </div>
                                
                                <div class= 'w-full flex bg-blue-200 rounded-lg '>
                                    <p class = "font-bold ">Cantidad:</p> 
                                    <input type= 'number' value = '1' class = 'w-8 pl-2 bg-transparent'> 
                                </div>
                            </div>`;

    // para poder almacenar los elementos sacandolo con DOM y no enviarlos directamente, encerraré el elemento con su nombre descripcion y demas en un div y le colocaré una id unica para definir diferentes o un conteo de elemento y poder diferenciarlos.


    panelList.appendChild(listItem);

    // Abrir panel en pantallas pequeñas
    if (window.innerWidth <= 640) {
        panel.classList.add('open');
    }
}

// Optional: Add functionality to toggle the panel
const panel = document.getElementById('panel');
function togglePanel() {
    panel.classList.toggle('open');
}