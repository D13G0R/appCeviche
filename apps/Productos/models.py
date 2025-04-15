from django.db import models

# Create your models here.

class Pedidos(models.Model):
    sub_total = models.FloatField(null = False, blank = False)
    total = models.FloatField(null = False, blank = False)
    estado = models.BooleanField(default = True)
    descripcion_pedido = models.TextField(null = False, blank = False)

class Productos(models.Model):
    nombre_producto = models.CharField(max_length= 50, null = False, blank = False)
    descripcion_producto = models.TextField(null = False, blank = False)
    precio_producto = models.FloatField(null = False, blank = False)

class Topics(models.Model):
    nombre_topic = models.CharField(max_length= 50, null = False, blank = False)
    descripcion_topic = models.TextField(null = False, blank = False)
    precio_topic = models.FloatField(null = False, blank = False)

class Pedido_Producto_Topic(models.Model):
    fk_pedido = models.BigIntegerField()
    fk_producto = models.BigIntegerField()
    cantidad_producto = models.IntegerField()
    detalle_producto = models.TextField(default = "ninguno")
    fk_topic = models.BigIntegerField()
    cantidad_topic = models.IntegerField()
    detalle_topics = models.TextField(default="ninguno") #debo corregir esa s al final de detalle_topics la S final no va

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

