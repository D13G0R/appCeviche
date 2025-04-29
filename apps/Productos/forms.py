from django import forms
from apps.Productos.models import Productos, Topics

class FormularioEditarProducto(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ("__all__")

        labels = {
            "nombre_producto" : "Nombre del Producto",
            "descripcion_producto": "Descripcion",
            "precio_producto" : "Precio",
        }
        widgets = {
             "nombre_producto" : forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa el nombre del producto"
             }),
            "descripcion_producto": forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa la descripcion del producto"
             }),
             "precio_producto" : forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa el precio del producto"
             })
        }

class FormularioEditarTopic(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ("__all__")
        labels = {
            "nombre_topic" : "Nombre del Topic",
            "descripcion_topic": "Descripcion",
            "precio_topic" : "Precio",
        }
        widgets = {
             "nombre_topic" : forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa el nombre del topic"
             }),
            "descripcion_topic": forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa la descripcion del topic"
             }),
             "precio_topic" : forms.TextInput(attrs = { 
                 "placeholder" : "Ingresa el precio del topic"
             })
        }