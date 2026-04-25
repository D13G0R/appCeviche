from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView

from django.shortcuts import render, redirect

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.db import IntegrityError
from apps.User.forms import LoginForm
from apps.Productos.models import Pedido_Producto, Pedidos

import logging
logger = logging.getLogger(__name__)


def registerUser(request):
    logger.info("Procesando registro de usuario.")
    if request.method != "POST":
        return render(request, "register.html", {"error" : "METODO NO PERMITIDO."}, status=400)
    try:
        firstNameReceived = request.POST["firstName"].strip()
        lastNameReceived = request.POST["lastName"].strip()
        userNameReceived = request.POST["username"].strip()
        emailReceived = request.POST["email"].strip()
        passwordReceived = request.POST["password"].strip()

        if not len(passwordReceived) > 8:
            return render (request, "register.html", {"message": "error, la contraseña debe tener 8 o mas caracteres."})
        
    except KeyError as e:
        return render(request, "register.html", {"message": "error, faltan datos por completar."}, status=400)
    
    try:
        validate_email(emailReceived)
    except ValidationError:
        return render(request, "register.html", {"message": "Error, Correo invalido."}, status = 400)
    
    if User.objects.filter(username = userNameReceived).exists():
        return render(request, "register.html", {"message": "Error, ese username ya existe."}, status = 403)

    User.objects.create_user(
        first_name=firstNameReceived,
        last_name = lastNameReceived, 
        username= userNameReceived, 
        email = emailReceived, 
        password = passwordReceived)
    
    return render(request, "login.html", {"message": "Usuario creado correctamente"})


def loginUser(request):
    logger.info("Procesando inicio de sesión.")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                return render(request, "login.html", {
                    "message": "Usuario o contraseña incorrectos",
                    "form": form
                })
        else:
            return render(request, "login.html", {
                "message": "Por favor complete todos los campos correctamente",
                "form": form
            })
    
    return render(request, "login.html", {
        "form": LoginForm(),
        "message": None
    })

def logoutUser(request):
    logger.info("Cerrando sesión de usuario.")
    logout(request)
    return redirect("loginUser")

class adminSales(ListView):
    """
    Muestra una lista de todos los pedidos con sus detalles completos,
    optimizada para evitar problemas de N+1 queries.
    """
    # 1. Modelo principal: Pedidos
    model = Pedidos
    
    # 2. Nombre del archivo de la plantilla
    template_name = "adminSales.html"
    
    # 3. Nombre de la lista de objetos en la plantilla (será 'pedidos')
    context_object_name = "pedidos"
    
    # 4. (Opcional pero recomendado) Paginación para no mostrar miles de pedidos a la vez
    paginate_by = 20

    def get_queryset(self):
        """
        Sobrescribimos este método para optimizar la consulta.
        """
        logger.info("Accediendo a la vista de administración de ventas.")
        # prefetch_related es la clave aquí. Le dice a Django: "Cuando obtengas
        # los pedidos, trae también todos los productos y topics asociados en
        # consultas adicionales y eficientes, en lugar de una por cada pedido".
        queryset = Pedidos.objects.prefetch_related(
            'detalle_pedido__fk_producto',                 # Precarga los productos de cada pedido
            'detalle_pedido__topics_de_producto__fk_topic' # Precarga los topics de cada producto
        ).order_by('-fecha_pedido') # Muestra los pedidos más recientes primero
        
        return queryset
