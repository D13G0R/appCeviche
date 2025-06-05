from rest_framework import serializers
from .models import Pedido_Producto_Topic, Topics, Pedidos
class PedidoProductoTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Producto_Topic
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = '__all__'  # O especifica solo los campos que necesites