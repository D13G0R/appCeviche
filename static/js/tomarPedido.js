// Array para almacenar los pedidos en formato JSON
let listaElementos = [];
let contador = 0; 

// Función para mostrar notificaciones profesionales
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? '✅' : '❌';
    
    toast.innerHTML = `
        <span>${icon}</span>
        <div>
            <p style="margin:0; font-weight:bold;">${type === 'success' ? 'Éxito' : 'Error'}</p>
            <p style="margin:0; font-size: 0.85rem; opacity: 0.8;">${message}</p>
        </div>
    `;
    
    container.appendChild(toast);
    
    // Forzar reflow para la animación
    setTimeout(() => toast.classList.add('show'), 10);
    
    // Eliminar automáticamente
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Función para agregar un elemento al panel
function addToPanel(tipo, id, nombre, precio = null) {
    const panelList = document.getElementById('panel-list');
    const listItem = document.createElement('li');
    contador ++;

    // Estilo y estructura del elemento
    listItem.className = "bg-[#1B263B] p-4 rounded shadow-md mb-4 border border-[rgba(224,229,236,0.1)] flex flex-col gap-2 elementos"; // Se añadió clase 'elementos' aquí
listItem.innerHTML = `
    <div class="id-${contador} flex flex-col gap-2"> 
        
        <input class="id_elemento" type="hidden" value="id-${contador}">

        
        <div class="w-full flex flex-row justify-between items-baseline border-b border-dashed border-[rgba(224,229,236,0.1)] pb-1 mb-1">
            <h3 class="tipo text-[#FF6B00] font-semibold text-xs uppercase tracking-wider">${tipo}</h3> 
            <p class="text-xs text-[#E0E5EC] bg-[#233451] px-2 py-0.5 rounded">${contador}</p> 
        </div>

        
        <div class="flex justify-between items-center text-sm"> 
            
            <input class="id_producto" type="hidden" value="${id}">
            
            <p class="nombre text-white font-medium text-sm truncate flex-grow mr-2">${nombre}</p>
            
            <div class="flex items-center gap-1 flex-shrink-0"> 
                <button class="increment-btn bg-[#233451] text-white rounded px-2 text-base font-semibold leading-tight cursor-pointer transition-colors duration-200 hover:bg-[#FF6B00]">+</button> 
                <div class="cantidad-container w-7 h-7 bg-[#FF6B00] rounded flex items-center justify-center flex-shrink-0"> 
                    <p class="cantidad_producto text-xs font-semibold text-white">1</p> 
                </div>
                <button class="decrement-btn bg-[#233451] text-white rounded px-2 text-base font-semibold leading-tight cursor-pointer transition-colors duration-200 hover:bg-[#FF6B00]">-</button> 
            </div>
        </div>

        
        <div class="flex justify-between items-center text-sm"> 
            
            ${precio ? `<p class="precioUnidad text-[#E0E5EC] text-xs hidden">${precio}</p>` : ''}
            
            <p class="font-medium text-[#E0E5EC]">Total</p> 
            
            ${precio ? `<p class="precio text-white font-bold">${precio}</p>` : ''} 
        </div>

      
        <div> 
            <textarea
                class="detalle_producto w-full h-12 p-2 mt-2 bg-[#233451] border border-[rgba(224,229,236,0.1)] rounded text-sm text-white resize-none transition-colors duration-200 ease-in-out focus:outline-none focus:border-[#FF6B00] placeholder-gray-500 placeholder:italic"
                placeholder="Detalle del pedido..."
            ></textarea>
        </div>

        
        <div> 
             <button
                class="add-topic-btn self-start mt-1 px-3 py-1 bg-[#FF6B00] text-white text-xs font-medium rounded border border-black/20 cursor-pointer transition-colors duration-200 hover:bg-[#E55A00]"
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
    
    // Abrir el panel automáticamente en pantallas pequeñas
    if (window.innerWidth <= 640) {
        const panel = document.getElementById('panel');
        panel.classList.add('open');
    }
}

// Función para alternar la visibilidad del panel
function togglePanel() {
    const panel = document.getElementById('panel');
    panel.classList.toggle('open');
}

// Event listener para manejar el incremento de cantidad
document.getElementById('panel-list').addEventListener('click', function(event) {
    const incrementBtn = event.target.closest('.increment-btn');
    const decrementBtn = event.target.closest('.decrement-btn');

    if (!incrementBtn && !decrementBtn) return;

    const idContainer = event.target.closest('li.elementos');
    if (!idContainer) return;

    const cantidadElement = idContainer.querySelector('.cantidad_producto');
    let cantidad = parseInt(cantidadElement.textContent);

    if (incrementBtn) {
        cantidad++;
    } else if (decrementBtn && cantidad > 1) {
        cantidad--;
    }

    cantidadElement.textContent = cantidad;
    actualizarTotalProducto(idContainer);
});

let currentProductTarget = null;
async function panelAddTopics(btn) {
    currentProductTarget = btn.closest('li.elementos'); 

    try {
        const response = await fetch("http://127.0.0.1:8000/api/topicsAll");
        if (!response.ok) throw new Error("Error al obtener topics");
        const data = await response.json();

        const modal = document.querySelector(".modalTopicss");
        modal.innerHTML = ''; 
        modal.classList.replace("hidden", "flex");
        
        const modalContent = document.createElement("div");
        modalContent.className = "bg-[#233451] rounded shadow-2xl border border-[rgba(224,229,236,0.1)] w-11/12 max-w-4xl overflow-hidden flex flex-col max-h-[90vh]";
        
        modalContent.innerHTML = `
            <div class="w-full bg-[#FF6B00] text-white p-4 flex justify-between items-center">
                <h2 class="text-lg font-bold">Seleccionar Topic</h2>
                <button onclick="closeTopicModal()" class="text-white hover:opacity-70 text-2xl">&times;</button>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6 overflow-y-auto">
                ${data.map(topic => `
                    <button onclick='addTopicToProduct(${JSON.stringify(topic)})' class="bg-[#1B263B] border border-[rgba(224,229,236,0.1)] rounded p-4 hover:border-[#FF6B00] transition text-left flex flex-col justify-between h-full group">
                        <div>
                            <div class="flex justify-between items-center mb-2">
                                <h3 class="text-[#FF6B00] font-bold">${topic.nombre_topic}</h3>
                                <span class="text-[10px] opacity-50">#${topic.id}</span>
                            </div>
                            <p class="text-[#E0E5EC] text-xs opacity-70 mb-4">${topic.descripcion_topic}</p>
                        </div>
                        <div class="flex justify-between items-center pt-2 border-t border-white/5">
                            <span class="text-white font-bold">$${topic.precio_topic}</span>
                            <span class="bg-[#FF6B00] text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition">AGREGAR</span>
                        </div>
                    </button>
                `).join('')}
            </div>
        `;
        modal.appendChild(modalContent);
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function closeTopicModal() {
    const modal = document.querySelector(".modalTopicss");
    modal.classList.replace("flex", "hidden");
    modal.innerHTML = '';
}

function addTopicToProduct(topic) {
    const topicWrapper = document.createElement("div");
    topicWrapper.className = "topic-item bg-[#233451] border border-[rgba(224,229,236,0.1)] rounded p-3 mt-2 topic-added";

    topicWrapper.innerHTML = `
        <div class="flex justify-between items-center mb-1">
            <input class="id_topic" type="hidden" value="${topic.id}">
            <p class="font-semibold text-white text-sm">${topic.nombre_topic}</p>
            <button class="remove-topic text-xs text-[#E06C75] font-bold">&times;</button>
        </div>
        <div class="flex items-center justify-between text-sm mb-1">
            <p class="text-[#E0E5EC] text-xs">Precio:</p>
            <p class="precio_topic font-medium text-[#FF6B00] text-xs">${topic.precio_topic}</p>
        </div>
        <div class="flex items-center gap-2 mb-2">
            <button class="inc-topic bg-[#1B263B] text-white px-2 rounded">-</button>
            <span class="cantidad_topic text-white text-xs">1</span>
            <button class="dec-topic bg-[#1B263B] text-white px-2 rounded">+</button>
        </div>
        <textarea class="detalle_topic w-full p-2 bg-[#1B263B] border border-[rgba(224,229,236,0.1)] rounded text-[10px] text-white resize-none" placeholder="Detalle..."></textarea>
    `;

    const basePrice = parseFloat(topic.precio_topic);
    const qtySpan = topicWrapper.querySelector(".cantidad_topic");
    const priceText = topicWrapper.querySelector(".precio_topic");

    topicWrapper.querySelector(".dec-topic").addEventListener("click", () => {
        let qty = parseInt(qtySpan.textContent);
        qty++;
        qtySpan.textContent = qty;
        priceText.textContent = (qty * basePrice).toFixed(2);
        actualizarTotalProducto(currentProductTarget);
    });

    topicWrapper.querySelector(".inc-topic").addEventListener("click", () => {
        let qty = parseInt(qtySpan.textContent);
        if (qty > 1) {
            qty--;
            qtySpan.textContent = qty;
            priceText.textContent = (qty * basePrice).toFixed(2);
            actualizarTotalProducto(currentProductTarget);
        }
    });

    topicWrapper.querySelector(".remove-topic").addEventListener("click", () => {
        topicWrapper.remove();
        actualizarTotalProducto(currentProductTarget);
    });

    currentProductTarget.querySelector('.id_producto').parentNode.parentNode.appendChild(topicWrapper);
    closeTopicModal();
    actualizarTotalProducto(currentProductTarget);
}

function actualizarTotalProducto(productDiv) {
    const basePrice = parseFloat(productDiv.querySelector(".precioUnidad").textContent);
    const productQty = parseInt(productDiv.querySelector(".cantidad_producto").textContent);
    let total = basePrice * productQty;

    const topics = productDiv.querySelectorAll(".topic-item");
    topics.forEach(topic => {
        total += parseFloat(topic.querySelector(".precio_topic").textContent);
    });

    productDiv.querySelector(".precio").textContent = total.toFixed(2);
    actualizarTotalPedido();
}

function actualizarTotalPedido() {  
    let totalText = document.querySelector(".totalPedido");  
    let itemPrices = document.querySelectorAll(".precio");  
    let grandTotal = 0;  

    itemPrices.forEach(price => {  
        grandTotal += parseFloat(price.textContent) || 0; 
    });  

    totalText.innerHTML = grandTotal.toFixed(2);
}  

async function enviarDatos() {
    listaElementos = []; // Limpiar antes de recolectar
    const elementosNodes = document.querySelectorAll("li.elementos");
    
    if (elementosNodes.length === 0) {
        showToast("No hay productos en el pedido", "error");
        return;
    }

    const detalle_pedido = document.querySelector(".textarea_descripcion_pedido").value.trim();

    elementosNodes.forEach(elemento => {
        const topics = [];
        elemento.querySelectorAll(".topic-added").forEach(topicNode => {
            topics.push({
                "id_topic": topicNode.querySelector(".id_topic").value,
                "cantidad_topic": topicNode.querySelector(".cantidad_topic").textContent,
                "detalle_topic": topicNode.querySelector(".detalle_topic").value
            });
        });

        listaElementos.push({
            "id_elemento": elemento.querySelector(".id_elemento").value,
            "descripcion_pedido": detalle_pedido,
            "precio_total": document.querySelector(".totalPedido").textContent,
            "precio_unidad_producto": elemento.querySelector(".precio").textContent,
            "producto": {
                "id_producto": elemento.querySelector(".id_producto").value,
                "cantidad_producto": elemento.querySelector(".cantidad_producto").textContent,
                "detalle_producto": elemento.querySelector(".detalle_producto").value,
                "topics": topics
            }
        });
    });

    try {
        const response = await fetch("http://127.0.0.1:8000/api/receiveOrder", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            credentials: "include",
            body: JSON.stringify(listaElementos),
        });

        const data = await response.json();
        
        if (response.ok) {
            showToast(data.message || "Pedido enviado correctamente");
            
            // LIMPIEZA TOTAL
            document.getElementById('panel-list').innerHTML = '';
            document.querySelector(".totalPedido").innerHTML = '0.00';
            document.querySelector(".textarea_descripcion_pedido").value = '';
            listaElementos = [];
            contador = 0;
        } else {
            showToast(data.detail || "Error al enviar el pedido", "error");
        }
    } catch (error) {
        showToast("Error de conexión", "error");
    }
}

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let c = cookie.trim();
        if (c.startsWith(name + '=')) return decodeURIComponent(c.substring(name.length + 1));
    }
    return null;
}

// Mobile compatibility
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.createElement('button');
    btn.className = 'md:hidden fixed bottom-6 right-6 z-50 bg-[#FF6B00] text-white p-4 rounded-full shadow-2xl';
    btn.innerHTML = '🛒';
    btn.onclick = togglePanel;
    document.body.appendChild(btn);
});
