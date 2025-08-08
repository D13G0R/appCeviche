async function changeDescription(id){
    let textarea = document.getElementById(`description-${id}`).value;

    let text = textarea.trim();

    const response = await fetch("http://127.0.0.1:8000/api/changeDescriptionOrder", {
        method : "PUT",
        headers: {
            "Content-Type" : "application/json",
             "X-CSRFToken": getCSRFToken(),  // 👈 CSRF obligatorio
        },
        body: JSON.stringify({
            order_id: id,
            new_description : text
        })
    })
    
    if(!response.ok){
        throw new Error('Error en la data de la response');
    }
    let data = await response.json();
    alert("Mensaje: " + data["message"], "Detalle: " + data["detail"]);
}


function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return null;
}