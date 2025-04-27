from django import forms
from apps.Productos.models import Productos

class FormularioEditarProducto(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ["nombre_producto", "descripcion_producto", "precio_producto"]

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
                 "placeholder" : "Ingresa el nombre del producto"
             })
        }
