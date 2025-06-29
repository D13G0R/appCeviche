from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view 

from .models import Pedido_Producto_Topic, Pedidos, Productos, Topics, Pedido_Producto
from .serializers import PedidoProductoTopicSerializer, TopicSerializer,  PedidoSerializer
from apps.Productos import forms

from django.utils import timezone
from django.db.models import Q
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
    hoy = timezone.datetime
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
            descripcion_pedido = elemento["descripcion_pedido"]
            pedido = Pedidos.objects.create(sub_total = precio_total, total = precio_total, estado = "Pendiente", descripcion = descripcion_pedido if descripcion_pedido else "Ninguna", fecha_pedido = hoy)
            seCreoPedido = True

        producto = elemento["producto"]
        id_producto = producto["id_producto"]
        OBJETO_producto = Productos.objects.get(id = id_producto)
        cantidad_producto = producto["cantidad_producto"]
        detalle_producto = producto["detalle_producto"]
        OBJETO_pedido_producto = Pedido_Producto.objects.create(fk_pedido = pedido, fk_producto = OBJETO_producto, cantidad_producto = cantidad_producto, detalle_producto = detalle_producto)
        if not OBJETO_pedido_producto:
            message = "ERROR al crear un pedido_producto"
            return  Response({"message": message})
        
        for topic in producto["topics"]:
            id_topic = topic["id_topic"]
            OBJETO_topic = Topics.objects.get(id = id_topic)
            cantidad_topic = topic["cantidad_topic"]
            detalle_topic = topic["detalle_topic"]
            pedido_producto_topic = Pedido_Producto_Topic.objects.create(fk_id_pedido_producto = OBJETO_pedido_producto, fk_topic = OBJETO_topic, cantidad_topic = cantidad_topic, detalle_topic = detalle_topic)
            if not pedido_producto_topic:
                message = "ERROR al crear un pedido_producto_topic"
                return  Response({"message": message})
           
    message = "Todo Ok (al parecer)"
    return  Response({"message": message})

class showOrdersTaken(ListView):
    model = Pedidos
    context_object_name = "Pedidos"
    template_name = "ordersTaken.html" # HAY QUE CAMBIAR ACA EL NOMBRE DEL HTML DESPUES DE ESTRUCTURAR
    def get_queryset(self):
        return Pedidos.objects.filter(estado = "Pendiente").prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
    
from django.utils import timezone
from datetime import datetime

class showAllOrders(ListView):
    model = Pedidos
    context_object_name = "Pedidos"
    template_name = "allOrders.html"
    hoy = timezone.localtime(timezone.now())
    dia_seleccionado = ""

    def get_queryset(self):
        dia_str = self.kwargs.get("dia")
        if dia_str:
            try:
                fecha_str = dia_str  # "YYYY-MM-DD"
                fecha_date = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                self.dia_seleccionado = fecha_date
                # La búsqueda en DB debe usar la parte de fecha únicamente
                return Pedidos.objects.filter(fecha_pedido__date=fecha_date).prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
            except ValueError:
                # Fecha inválida, usas hoy o ajustas como quieras
                return Pedidos.objects.none()  # O Pedidos.objects.filter(fecha_pedido__date=self.hoy.date())
        else:
            # Sin parámetro, filtrar por hoy
            return Pedidos.objects.filter(fecha_pedido__date=self.hoy.date()).prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
            self.dia_seleccionado = hoy
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hoy"] = self.dia_seleccionado
        return context
    
# @api_view(['POST'])
# def filtrarFecha(request):
#     print(f"REQUEST : {request}")
#     data = json.loads(request.body)
#     print(f"DATA:{data}")
#     date = data.get("date")
#     print(f"FECHA: {date}")
#     pedidos = Pedidos.objects.filter(fecha_pedido__icontains = date).prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
#     pedidosSerializado = PedidoSerializer(pedidos, many = True)
#     return Response({"pedidos" : pedidosSerializado.data})


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
    




class adminProductos(ListView):
    model = Productos
    template_name = "adminProductos.html"
    # context_object_name = "Objetos_productos"

class crearProducto(CreateView):
    model = Productos
    template_name="formularioCrearProducto.html"
    success_url = reverse_lazy("adminProductos")
    form_class = forms.FormularioEditarProducto

class editarProducto(UpdateView):
    model = Productos
    form_class = forms.FormularioEditarProducto
    success_url = reverse_lazy("adminProductos")
    template_name = "formularioEditarProducto.html"

class eliminarProducto(DeleteView):
    model = Productos
    template_name = "confirmDeleteProducto.html"
    success_url= reverse_lazy("adminProductos")
    context_object_name = "Producto"

def deshabilitarProducto(request, id):
    producto_id = id
    objetoProducto = Productos.objects.get(id = id)
    objetoProducto.estado_producto = "Deshabilitado"
    objetoProducto.save()
    return redirect("adminProductos")

def activarProducto(request, id):
    objectoProducto = Productos.objects.get(id = id)
    objectoProducto.estado_producto = "Activo"
    objectoProducto.save()
    return redirect("adminTopics")




class adminTopics(ListView):
    model = Topics
    template_name = "adminTopics.html"
    # context_object_name = "ObjetoTopics"

class crearTopic(CreateView):
    model = Topics
    template_name = "formularioCrearTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic

class editarTopic(UpdateView):
    model = Topics
    template_name = "formularioEditarTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic

class eliminarTopic(DeleteView):
    model = Topics
    template_name = "confirmDeleteTopic.html"
    success_url = reverse_lazy("adminTopics")
    context_object_name = "Topic"

def deshabilitarTopic(request, id):
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Deshabilitado"
    objectoTopic.save()
    return redirect("adminTopics")

def activarTopic(request, id):
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Activo"
    objectoTopic.save()
    return redirect("adminTopics")