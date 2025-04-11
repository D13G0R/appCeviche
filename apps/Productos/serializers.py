from rest_framework import serializers
from .models import Pedido_Producto_Topic, Topics
class PedidoProductoTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido_Producto_Topic
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = '__all__'
