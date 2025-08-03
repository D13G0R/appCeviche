from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def register(request):
    if request != "POST":
        return render(request, "register.html", {"message" : "METODO NO PERMITIDO."}, status=400)
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