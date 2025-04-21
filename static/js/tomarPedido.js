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
    listItem.className = "bg-white p-4 rounded-lg shadow-md mb-4 border border-gray-300";
    listItem.innerHTML = `
        <div class="id-${contador} elementos flex flex-col gap-1">
            <input class = "id_elemento" type = "hidden" value ="id-${contador}">
            <div class = "w-full flex flex-row justify-between">
                <h3 class="tipo font-bold text-sm text-gray-700">${tipo}</h3>
                <p class = "text-sm">${contador}</p>
            </div>

        
            <div class="flex justify-between items-center text-sm">
                <input class = "id_producto" type = "hidden" value ="${id}">
                <p class="nombre font-medium text-gray-600">${nombre}</p>
                <div class="flex items-center gap-1">
                    <button class="increment-btn text-sm font-bold bg-gray-200 px-1 rounded hover:bg-gray-300">+</button>
                    <div class="cantidad-container w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center">
                        <p class="cantidad_producto text-xs font-semibold text-white">1</p>
                    </div>
                    <button class="decrement-btn text-sm font-bold bg-gray-200 px-1 rounded hover:bg-gray-300">-</button>
                </div>
            </div>
            <div class="flex justify-between items-center text-sm">
${precio ? `<p class="precioUnidad text-gray-800 font-bold hidden">${precio}</p>` : ''}
                <p class="font-medium text-gray-600">Total</p>
                ${precio ? `<p class="precio text-gray-800 font-bold">${precio}</p>` : ''}
                
            </div>
            <div>
                <textarea class="detalle_producto w-full h-12 p-1 mt-2 border rounded text-sm text-gray-700 resize-none" placeholder="Detalle del pedido..."></textarea>
            </div>
            <button class="add-topic-btn w-1/2 py-1 bg-blue-500 text-sm text-white font-medium rounded border border-black hover:bg-blue-400" onclick="panelAddTopics(this)">
                Agregar Topic
            </button>
        </div>
    `;

    // Agregar el elemento al panel
    panelList.appendChild(listItem);
    actualizarTotalPedido()
    // Abrir el panel automáticamente en pantallas pequeñas
    if (window.innerWidth <= 640) {
        panel.classList.add('open');
    }
}

// Función para alternar la visibilidad del panel
const panel = document.getElementById('panel');
function togglePanel() {
    panel.classList.toggle('open');
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



//MODIFICADO POR IA
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
        const modal = document.querySelector(".modalTopics");
        modal.innerHTML = ''; // Limpia antes de renderizar
        modal.classList.replace("hidden", "absolute");

        data.forEach(element => {
            const card = document.createElement("button");
            card.className = "topicRelated bg-white shadow-lg border border-gray-300 rounded-lg p-4 w-64 hover:shadow-xl transition duration-300 ease-in-out";
            card.innerHTML = `
                <h3 class="text-blue-600 font-bold text-lg mb-2" data-id="${element.id}" data-nombre="${element.nombre_topic}" data-precio="${element.precio || 100}">#${element.id} - ${element.nombre_topic}</h3>
                <p class="text-gray-700 text-sm">${element.descripcion_topic}</p>
            `;
            card.addEventListener("click", () => addTopicToProduct(element));
            modal.appendChild(card);
        });
    }
}//END IA

function closeTopicModal() {
    const modal = document.querySelector(".modalTopics");
    modal.classList.replace("absolute", "hidden");
}

//START IA (AGREGAR TOPIC A UN PRODUCTO)
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










let listaElementos = [];
async function enviarDatos (){
    elementos = document.querySelectorAll(".elementos").forEach(elemento => {
        let id_elemento = elemento.querySelector(".id_elemento").value;//input

        let id_producto = elemento.querySelector(".id_producto").value;//input
        let cantidad_producto = elemento.querySelector(".cantidad_producto").textContent; //p
        let detalle_producto = elemento.querySelector(".detalle_producto") ? elemento.querySelector(".detalle_producto").value : ""; //textarea
        

        let id_topic = elemento.querySelector(".id_topic") ? elemento.querySelector(".id_topic").value : 0; //input
        let cantidad_topic = elemento.querySelector(".cantidad_topic") ? elemento.querySelector(".cantidad_topic").textContent : 0; //span
        let detalle_topic = elemento.querySelector(".detalle_topic") ? elemento.querySelector(".detalle_topic").value : ""; //textarea

        let precioTotal = document.querySelector(".totalPedido").textContent;
        let precioUnidad = elemento.querySelector(".precioUnidad").textContent;//NO SE ESTÁ USANDO AUN

        let dicElemento = 
        {
            "id_elemento" : id_elemento,
            "precio_total" : precioTotal,
            "precio_unidad_producto": precioTotal,  
            "elemento": 
                {
                    "id_producto" : id_producto,
                    "cantidad_producto" : cantidad_producto,
                    "detalle_producto" : detalle_producto,
                    "id_topic" : id_topic,
                    "cantidad_topic": cantidad_topic,
                    "detalle_topic" : detalle_topic
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
    .then(data => console.log(data));
}
//END IA