from django.db import models
from .choices import estados_productos
# Create your models here.

class Pedidos(models.Model):
    sub_total = models.FloatField(null = False, blank = False)
    total = models.FloatField(null = False, blank = False)
    estado = models.CharField(max_length=15, null = False, blank = False, default = "Pendiente")
    descripcion = models.TextField(null = False, blank = False)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

class Productos(models.Model):
    nombre_producto = models.CharField(max_length= 50, null = False, blank = False)
    descripcion_producto = models.TextField(null = False, blank = False)
    precio_producto = models.FloatField(null = False, blank = False)
    estado_producto = models.TextField(choices = estados_productos, default = "activo")
    fecha_lanzado = models.DateTimeField(auto_now_add=True)

class Pedido_Producto(models.Model):
    fk_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, related_name="detalle_pedido")
    fk_producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    detalle_producto = models.TextField(null = True, blank = True)


class Topics(models.Model):
    nombre_topic = models.CharField(max_length= 50, null = False, blank = False)
    descripcion_topic = models.TextField(null = False, blank = False)
    precio_topic = models.FloatField(null = False, blank = False)
    estado_topic = models.TextField(choices = estados_productos, default = "activo")
    fecha_lanzado= models.DateTimeField(auto_now_add=True)

class Pedido_Producto_Topic(models.Model):
    fk_id_pedido_producto = models.ForeignKey(Pedido_Producto, on_delete=models.CASCADE, related_name = "topics_de_producto")
    fk_topic = models.ForeignKey(Topics, related_name = "topics", on_delete=models.CASCADE, null = True)
    cantidad_topic = models.IntegerField()
    detalle_topic = models.TextField(default="ninguno", blank = True)

# [
#     {
#     fk_pedido: 
#         [
#             {
#                 fk_producto : cantidad
#                 detalle : Detalle
#             },
#             {
#                 fk_topic : cantidad
#                 detalle : Detalle
#             }

#         ]
#     }
# ]

#Representación JSON comentada del modelo Pedido_Producto_Topic:
# [
#     {
#         "fk_pedido": 1,  # ID del pedido
#         "productos": [  # Lista de productos asociados al pedido
#             {
#                 "fk_producto": 101,  # ID del producto
#                 "cantidad_producto": 2,  # Cantidad del producto
#                 "detalle_producto": "Detalle del producto 1"  # Detalle del producto
#             },
#             {
#                 "fk_producto": 102,
#                 "cantidad_producto": 1,
#                 "detalle_producto": "Detalle del producto 2"
#             }
#         ],
#         "topics": [  # Lista de topics asociados al pedido
#             {
#                 "fk_topic": 201,  # ID del topic
#                 "cantidad_topic": 3,  # Cantidad del topic
#                 "detalle_topics": "Detalle del topic 1"  # Detalle del topic
#             },
#             {
#                 "fk_topic": 202,
#                 "cantidad_topic": 1,
#                 "detalle_topics": "Detalle del topic 2"
#             }
#         ]
#     }
# ]

