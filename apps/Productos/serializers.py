from rest_framework import serializers
from .models import Pedido_Producto_Topic

class PedidoProductoTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Producto_Topic
        fields = '__all__'