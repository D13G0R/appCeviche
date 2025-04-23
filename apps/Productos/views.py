from django.shortcuts import render, redirect
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

#HAY QUE CONTIUAR CON MOSTRAR LOS PEDIDOS QUE SE HAYAN ECHO.
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
            pedido = Pedidos.objects.create(sub_total = precio_total, total = precio_total, estado = "Pendiente", descripcion_pedido ="Ninguna")
            seCreoPedido = True

        producto = elemento["producto"]
        id_producto = producto["id_producto"]
        cantidad_producto = producto["cantidad_producto"]
        detalle_producto = producto["detalle_producto"]

        for topic in producto["topics"]:
            id_topic = topic["id_topic"]
            cantidad_topic = topic["cantidad_topic"]
            detalle_topic = topic["detalle_topic"]
            
            jsonFormatData = {
                "fk_pedido" : int(pedido.id),
                "fk_producto" : int(id_producto),
                "cantidad_producto" : int(cantidad_producto),
                "detalle_producto" : detalle_producto if detalle_producto else "sin detalle", #HAY QUE CREAR UNA TABLA POR PRODUCTO SELECCIONADO Y POR TOPICS Y LUEGO UNIRLAS EN UNA TABLA INTERMEDIA PARA QUE NO HAYA REDUNDANCIA
                "fk_topic" : int(id_topic) if id_topic else int(100),
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

class showOrdersTaken(ListView):
    model = Pedidos
    context_object_name = "orders"
    template_name = "ordersTaken.html"
    def get_queryset(self):
        return Pedidos.objects.filter(estado = "Pendiente")

def cancelarPedido(request, id):
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Cancelado"
    pedido.save()
    return redirect("showOrdersTaken")

def pagarPedido(request, id):
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Pagado"
    pedido.save()
    return redirect("showOrdersTaken")
    