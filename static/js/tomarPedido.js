// Array para almacenar los pedidos en formato JSON
let pedidoJson = [];
let contador = 0; //HAY QUE ARREGLAR ACA YA QUE SI SE INCREMENTA LA CANTIDAD DE TOPICS Y LUEGO LA CANTIDAD DE PRODUCTOS EL TOTAL RETROCEDE SUMANDO SOLO LOS PRODUCTOS 
// Y NO LOS YOPICS PERO SI VUELVES SUMAR O RESTAR UN TOPIC VUELVE A LA NORMALIDAD
// Función para agregar un elemento al panel
function addToPanel(tipo, id, nombre, precio = null) {
    const panelList = document.getElementById('panel-list');
    const listItem = document.createElement('li');
    contador ++;

    // Estilo y estructura del elemento
    listItem.className = "bg-white p-4 rounded-lg shadow-md mb-4 border border-gray-300 flex flex-col gap-2"; // Added flex, flex-col, gap-2
listItem.innerHTML = `
    <div class="id-${contador} elementos flex flex-col gap-2"> 
        
        <input class="id_elemento" type="hidden" value="id-${contador}">

        
        <div class="w-full flex flex-row justify-between items-baseline border-b border-dashed border-gray-300 pb-1 mb-1">
            <h3 class="tipo text-gray-600 font-semibold text-xs uppercase tracking-wider">${tipo}</h3> 
            <p class="text-xs text-gray-500 bg-gray-200 px-2 py-0.5 rounded-full">${contador}</p> 
        </div>

        
        <div class="flex justify-between items-center text-sm"> 
            
            <input class="id_producto" type="hidden" value="${id}">
            
            <p class="nombre text-gray-800 font-medium text-sm truncate flex-grow mr-2">${nombre}</p>
            
            <div class="flex items-center gap-1 flex-shrink-0"> 
                <button class="increment-btn bg-gray-200 text-gray-600 rounded px-2 text-base font-semibold leading-tight cursor-pointer transition-colors duration-200 hover:bg-gray-300 hover:text-gray-800">+</button> 
                <div class="cantidad-container w-7 h-7 bg-blue-500 rounded-full flex items-center justify-center flex-shrink-0"> 
                    <p class="cantidad_producto text-xs font-semibold text-white">1</p> 
                </div>
                <button class="decrement-btn bg-gray-200 text-gray-600 rounded px-2 text-base font-semibold leading-tight cursor-pointer transition-colors duration-200 hover:bg-gray-300 hover:text-gray-800">-</button> 
            </div>
        </div>

        
        <div class="flex justify-between items-center text-sm"> 
            
            ${precio ? `<p class="precioUnidad text-gray-500 text-xs hidden">${precio}</p>` : ''}
            
            <p class="font-medium text-gray-600">Total</p> 
            
            ${precio ? `<p class="precio text-gray-800 font-bold">${precio}</p>` : ''} 
        </div>

      
        <div> 
            <textarea
                class="detalle_producto w-full h-12 p-2 mt-2 border border-gray-300 rounded-lg text-sm text-gray-800 resize-none transition-colors duration-200 ease-in-out focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 placeholder-gray-400 placeholder:italic"
                placeholder="Detalle del pedido..."
            ></textarea>
        </div>

        
        <div> 
             <button
                class="add-topic-btn self-start mt-1 px-3 py-1 bg-blue-500 text-white text-xs font-medium rounded-lg border border-black/20 cursor-pointer transition-colors duration-200 hover:bg-blue-600"
                onclick="panelAddTopics(this)"
             >
                Agregar Topic
            </button>
        </div>
    </div>
`;

    // Agregar el elemento al panel
    panelList.appendChild(listItem);
    actualizarTotalPedido();
    
    // Abrir el panel automáticamente en pantallas pequeñas y asegurar que sea visible
    if (window.innerWidth <= 640) {
        const panel = document.getElementById('panel');
        panel.classList.add('open');
        panel.style.zIndex = "999";
        panel.style.display = "block";
    }
}

// Función para alternar la visibilidad del panel
const panel = document.getElementById('panel');
function togglePanel() {
    panel.classList.toggle('open');
    
    // Asegurar visibilidad en móvil cuando se activa
    if (panel.classList.contains('open') && window.innerWidth <= 640) {
        panel.style.zIndex = "999";
        panel.style.display = "block";
    }
}

// Event listener para manejar el incremento de cantidad (opcional)
document.getElementById('panel-list').addEventListener('click', function(event) {
    const incrementBtn = event.target.closest('.increment-btn');
    const decrementBtn = event.target.closest('.decrement-btn');

    if (!incrementBtn && !decrementBtn) return;

    const idContainer = event.target.closest('div[class^="id-"]');
    if (!idContainer) return;

    const cantidadElement = idContainer.querySelector('.cantidad_producto');
    let cantidad = parseInt(cantidadElement.textContent);

    if (incrementBtn) {
        cantidad++;
    } else if (decrementBtn && cantidad > 1) {
        cantidad--;
    }

    cantidadElement.textContent = cantidad;

    // ✅ Actualizar el total completo del producto con topics incluidos
    actualizarTotalProducto(idContainer);
});



//MODIFICADO POR IA // USAMOS UNA URL PARA TRAER TODOS LOS TOPICS QUE HAYAN Y MOSTRARLO EN EL MODAL

let currentProductTarget = null;
async function panelAddTopics(btn) {
    currentProductTarget = btn.closest('div[class^="id-"]'); // Guardamos el producto donde se abrirá el modal

    const response = await fetch("http://127.0.0.1:8000/api/topicsAll", {
        "method": "GET",
        "headers": { "Content-Type": "application/json" }
    });

    if (!response.ok) throw new Error("Error en el response: ", response.status);

    const data = await response.json();
    console.log(data);

    if (data) {
        const modal = document.querySelector(".modalTopicss");
        modal.innerHTML = ''; // Limpia antes de renderizar
        modal.classList.replace("hidden", "absolute");
        
        // Añadir título al panel
        const titleContainer = document.createElement("div");
        titleContainer.className = "w-full bg-blue-500 text-white p-3 rounded-t-lg mb-4 flex justify-between items-center";
        titleContainer.innerHTML = `
            <h2 class="text-lg font-bold">Seleccionar Topic</h2>
            <button id="close-topic-modal" class="text-white hover:text-gray-200">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        `;
        modal.appendChild(titleContainer);
        
        // Crear contenedor para la cuadrícula de topics
        const gridContainer = document.createElement("div");
        gridContainer.className = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4 max-h-96 overflow-y-auto";
        modal.appendChild(gridContainer);
        
        // Estilizar el modal principal
        modal.className = "absolute bg-white rounded-lg shadow-2xl border border-gray-300 w-11/12 md:w-3/4 lg:w-2/3 max-w-4xl z-50 left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 modalTopicss";

        // Añadir cada topic como una tarjeta en la cuadrícula
        data.forEach(element => {
            const card = document.createElement("button");
            card.className = "topicRelated bg-white shadow-md border border-gray-300 rounded-lg p-4 hover:shadow-xl hover:border-blue-300 transition duration-300 ease-in-out flex flex-col justify-between h-full";
            card.innerHTML = `
                <div>
                    <div class="flex justify-between items-center mb-2">
                        <h3 class="text-blue-600 font-bold text-lg" data-id="${element.id}" data-nombre="${element.nombre_topic}" data-precio="${element.precio || 100}">${element.nombre_topic}</h3>
                        <span class="bg-gray-200 text-gray-700 px-2 py-1 rounded-full text-xs">#${element.id}</span>
                    </div>
                    <p class="text-gray-700 text-sm mb-2">${element.descripcion_topic}</p>
                </div>
                <div class="mt-2 flex justify-between items-center">
                    <span class="text-green-600 font-bold">${element.precio_topic || 100}</span>
                    <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">Agregar</span>
                </div>
            `;
            card.addEventListener("click", () => addTopicToProduct(element));
            gridContainer.appendChild(card);
        });
        
        // Agregar botones de acción en la parte inferior
        const actionContainer = document.createElement("div");
        actionContainer.className = "flex justify-end gap-3 p-4 bg-gray-100 rounded-b-lg border-t border-gray-300";
        
        const cancelButton = document.createElement("button");
        cancelButton.className = "px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition duration-200";
        cancelButton.textContent = "Cancelar";
        cancelButton.addEventListener("click", closeTopicModal);
        actionContainer.appendChild(cancelButton);
        
        modal.appendChild(actionContainer);
        
        // Añadir evento de cierre al botón de cerrar
        document.getElementById("close-topic-modal").addEventListener("click", closeTopicModal);
        
        // Añadir un overlay para mejorar el enfoque en el modal
        const overlay = document.createElement("div");
        overlay.className = "fixed inset-0 bg-black bg-opacity-50 z-40";
        overlay.id = "modal-overlay";
        overlay.addEventListener("click", closeTopicModal);
        document.body.appendChild(overlay);
    }
}
//END IA

//====================================CERRAR MODAL DE TOPICS MANUALMENTE
function closeTopicModal() {
    const modal = document.querySelector(".modalTopicss");
    modal.classList.replace("absolute", "hidden");
    
    const overlay = document.getElementById("modal-overlay");
    if (overlay) {
        overlay.remove();
    }
}

//====================================START IA (AGREGAR TOPIC A UN PRODUCTO) ====Debo echarle una repasada
function addTopicToProduct(topic) {
    const topicWrapper = document.createElement("div");
    topicWrapper.className = "topic-item bg-yellow-100 border border-blue-300 rounded p-2 mt-2";

    topicWrapper.innerHTML = `
        <div class="flex justify-between items-center mb-1">
            <input class = "id_topic "type="hidden" value = "${topic.id}">
            <p class="font-semibold text-gray-800 text-sm">${topic.nombre_topic}</p>
            <button class="remove-topic text-xs text-red-500 font-bold">X</button>
        </div>
        <div class="flex items-center justify-between text-sm mb-1">
            <p>Precio:</p>
            <p class="precio_topic font-medium">${topic.precio_topic || 100}</p>
        </div>
        <div class="flex items-center gap-2 mb-2">
            <button class="inc-topic bg-gray-300 px-2 rounded">+</button>
            <span class="cantidad_topic">${1}</span>
            <button class="dec-topic bg-gray-300 px-2 rounded">-</button>
        </div>
        <textarea class="detalle_topic w-full p-1 border rounded text-sm" placeholder="Detalle del topic..."></textarea>

    `;

    const precioBase = parseFloat(topic.precio_topic || 100);
    const cantidadSpan = topicWrapper.querySelector(".cantidad_topic");
    const precioText = topicWrapper.querySelector(".precio_topic");

    topicWrapper.querySelector(".inc-topic").addEventListener("click", () => {
        let cantidad = parseInt(cantidadSpan.textContent);
        cantidad++;
        cantidadSpan.textContent = cantidad;
        precioText.textContent = (cantidad * precioBase).toFixed(2);
        actualizarTotalProducto(currentProductTarget);
    });

    topicWrapper.querySelector(".dec-topic").addEventListener("click", () => {
        let cantidad = parseInt(cantidadSpan.textContent);
        if (cantidad > 1) {
            cantidad--;
            cantidadSpan.textContent = cantidad;
            precioText.textContent = (cantidad * precioBase).toFixed(2);
            actualizarTotalProducto(currentProductTarget);
        }
    });

    topicWrapper.querySelector(".remove-topic").addEventListener("click", () => {
        topicWrapper.remove();
        actualizarTotalProducto(currentProductTarget);
    });

    const topicContainer = document.createElement("div");
    topicContainer.className = "topic-added";
    topicContainer.appendChild(topicWrapper);

    currentProductTarget.appendChild(topicContainer);
    closeTopicModal();
    actualizarTotalProducto(currentProductTarget);
}




//====================================ACTUALIZAR TOTAL DE CADA PRODUCTO SEGUN SU CANTIDAD Y LOS TOPICS QUE TENGA TAMBIEN CON SU RESPECTICA CANTIDAD CADA UNO


function actualizarTotalProducto(productDiv) {
    const precioUnidadElement = productDiv.querySelector(".precioUnidad");
    const cantidadProducto = parseInt(productDiv.querySelector(".cantidad_producto").textContent);
    const base = parseFloat(precioUnidadElement.textContent);
    let total = base * cantidadProducto;

    const topics = productDiv.querySelectorAll(".topic-item");
    topics.forEach(topic => {
        const cantidadTopic = parseInt(topic.querySelector(".cantidad_topic").textContent);
        const precioUnitario = parseFloat(topic.querySelector(".precio_topic").textContent) / cantidadTopic;
        total += precioUnitario * cantidadTopic;
    });

    const precioTotal = productDiv.querySelector(".precio");
    precioTotal.textContent = total.toFixed(2);
    actualizarTotalPedido();
}




//====================================ACTUALIZAR TOTAL DEL PEDIDO



function actualizarTotalPedido() {  
    let totalText = document.querySelector(".totalPedido");  
    let preciosProductos = document.querySelectorAll(".precio");  
    let sumaTotal = 0;  

    preciosProductos.forEach(precioProducto => {  
        // Convert the text content to a number and add it to sumaTotal  
        sumaTotal += parseFloat(precioProducto.textContent) || 0; // Use parseFloat to convert to number  
    });  

    totalText.innerHTML = `${sumaTotal.toFixed(2)}`; // Display total with two decimal places  
}  

//====================================ENVIAR DATOS

let listaElementos = [];
async function enviarDatos (){
    elementos = document.querySelectorAll(".elementos").forEach(elemento => {
        let id_elemento = elemento.querySelector(".id_elemento").value;//input

        let detalle_pedido = document.querySelector(".textarea_descripcion_pedido").value.trim();

        let id_producto = elemento.querySelector(".id_producto").value;//input
        let cantidad_producto = elemento.querySelector(".cantidad_producto").textContent; //p
        let detalle_producto = elemento.querySelector(".detalle_producto") ? elemento.querySelector(".detalle_producto").value : ""; //textarea
        

        

        let topics = [];
        elemento.querySelectorAll(".topic-added").forEach(topic => {
            console.log(topic)
            let id_topic = topic.querySelector(".id_topic") ? topic.querySelector(".id_topic").value : 0; //input
            let cantidad_topic = topic.querySelector(".cantidad_topic") ? topic.querySelector(".cantidad_topic").textContent : 0; //span
            let detalle_topic = topic.querySelector(".detalle_topic") ? topic.querySelector(".detalle_topic").value : ""; //textarea
            console.log(id_topic)
            topics.push({
                    "id_topic" : id_topic,
                    "cantidad_topic": cantidad_topic,
                    "detalle_topic" : detalle_topic
            })
        });

        let precioTotal = document.querySelector(".totalPedido").textContent;
        let precioUnidad = elemento.querySelector(".precioUnidad").textContent;//NO SE ESTÁ USANDO AUN

        console.log(topics);
        let dicElemento = 
        {
            "id_elemento" : id_elemento,
            "descripcion_pedido" : detalle_pedido,
            "precio_total" : precioTotal,
            "precio_unidad_producto": precioTotal,  
            "producto": 
                {
                    "id_producto" : id_producto,
                    "cantidad_producto" : cantidad_producto,
                    "detalle_producto" : detalle_producto,
                    "topics" : topics
                }
        }
        listaElementos.push(dicElemento);
    });
    let JSONElements = JSON.stringify(listaElementos)
    console.log(JSONElements);

    const response = await fetch("http://127.0.0.1:8000/api/receiveOrder", {
        "method" : "POST",
        "headers" : {"Content-Type": "application/json"},
        "body" : JSON.stringify(listaElementos),
    })
    .then(res => res.json())
    .then(data => alert("Mensaje: " + data["message"], "Detalle: " + data["detail"] ));
}


//ESTO FUE DADO POR LA IA PARA QUE EN EL PANEL EN DISPOSICION PEQUEÑA (TELEFONO) SE VEAN LOS PRODUCTOS SELECCIONADOS

document.addEventListener('DOMContentLoaded', function() {
    const panelToggle = document.createElement('button');
    panelToggle.className = 'panel-toggle fixed bottom-4 right-4 z-50 bg-blue-500 text-white p-3 rounded-full shadow-lg';
    panelToggle.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>';
    
    panelToggle.addEventListener('click', function() {
        togglePanel();
    });
    
    document.body.appendChild(panelToggle);
    
    // Agregar listener para cambios de tamaño de pantalla
    window.addEventListener('resize', function() {
        const panel = document.getElementById('panel');
        
        if (window.innerWidth <= 640) {
            // Si es móvil y el panel debe estar abierto
            if (panel.classList.contains('open')) {
                panel.style.zIndex = "999";
                panel.style.display = "block";
            }
        } else {
            // Restablecer estilos en pantallas grandes
            panel.style.removeProperty('z-index');
            panel.style.removeProperty('display');
        }
    });
    
    // Añadir estilos CSS para móvil
    const styleSheet = document.createElement("style"); //LA ALTURA DE #panel acomoda la alltura del panel en la disposicion
    styleSheet.innerHTML = `
        @media (max-width: 640px) {
            #panel {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 30% !important; 
                background-color: transparent !important;
                z-index: 999;
                overflow-y: auto;
                padding: 1rem;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                
            }
            
            #panel.open {
                transform: translateX(0);
            }
            
            .modalTopics {
                position: fixed !important;
                z-index: 1000;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
                padding: 1rem;
            }
            
            .panel-toggle {
                display: block !important;
            }
        }
    `;
    document.head.appendChild(styleSheet);
});
//END IA