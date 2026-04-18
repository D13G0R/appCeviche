from django.contrib import admin
from apps.Productos.models import Pedidos, Pedido_Producto, Topics, Pedido_Producto_Topic

admin.site.register(Pedidos)
admin.site.register(Pedido_Producto)
admin.site.register(Topics)
admin.site.register(Pedido_Producto_Topic)