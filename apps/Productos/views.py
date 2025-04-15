from django.shortcuts import render
from django.views.generic import View, ListView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view 
from .models import Pedido_Producto_Topic, Pedidos, Productos, Topics
from .serializers import PedidoProductoTopicSerializer, TopicSerializer


# Create your views here.
class view_take_order(ListView):
    model = Productos
    context_object_name = "Productos"
    template_name = "tomarPedido.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Topics"] = Topics.objects.all().order_by("nombre_topic")
        return context
    

class PedidoProductoTopicView(APIView):
    def post(self, request):
        serializer = PedidoProductoTopicSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all().order_by("nombre_topic")
    serializer_class = TopicSerializer

@api_view(['POST'])
def receiveOrder(request):
    data = request.data
    if data:
        print(data)
        print("Datos Correctos")
    else:
        print("No llegaron datos")
    seCreoPedido = False
    for elemento in data:
        id_elemento = elemento["id_elemento"]
        precio_total = elemento["precio_total"]
        precio_unidad_producto = elemento["precio_unidad_producto"]

        if seCreoPedido != True:
            pedido = Pedidos.objects.create(sub_total = precio_total, total = precio_total, estado = True, descripcion_pedido ="Ninguna")
            seCreoPedido = True

        fragmentoElement = elemento["elemento"]
        id_producto = fragmentoElement["id_producto"]
        cantidad_producto = fragmentoElement["cantidad_producto"]
        detalle_producto = fragmentoElement["detalle_producto"]
        id_topic = fragmentoElement["id_topic"]
        cantidad_topic = fragmentoElement["cantidad_topic"]
        detalle_topic = fragmentoElement["detalle_topic"]
        jsonFormatData = {
            "fk_pedido" : int(pedido.id),
            "fk_producto" : int(id_producto),
            "cantidad_producto" : int(cantidad_producto),
            "detalle_producto" : detalle_producto if detalle_producto else "sin detalle",
            "fk_topic" : int(id_topic) if id_topic else int(0),
            "cantidad_topic" : int(cantidad_topic) if id_topic else int(0),
            "detalle_topics" : detalle_topic if id_topic else "sin detalle"  # OJO con el nombre correcto
        }
        
        serializer = PedidoProductoTopicSerializer(data=jsonFormatData)
        if serializer.is_valid():
            serializer.save()
            message = "Datos guardados correctamente"
        else:
            print(serializer.errors)
            message = "ERROR no se enviaron los datos o hay error en el formato."

    return  Response({"message": message})