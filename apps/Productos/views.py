# Django imports
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError, DataError
from datetime import datetime

# Django REST Framework imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError as DRFValidationError

# Local imports
from .models import Pedido_Producto_Topic, Pedidos, Productos, Topics, Pedido_Producto
from .serializers import PedidoProductoTopicSerializer, TopicSerializer, PedidoSerializer
from apps.Productos import forms
# Create your views here.


class view_take_order(LoginRequiredMixin, ListView):
    '''
    Vista para tomar ordenes

    Esta vista envia los productos y topics al html para poder tomar pedidos

    attributes:
        model = Usa el modelo Producto.
        context_object_name = Para no usar object_list usamos Productos para usar el contexto.
        template_name = plantilla donde se enviarán los datos.

    method:
        get_context_data() = trae y agrega al context los topics que estén registrados 
    '''
    model = Productos
    context_object_name = "Productos"
    template_name = "tomarPedido.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Topics"] = Topics.objects.all().order_by("nombre_topic")
        return context

class PedidoProductoTopicView(APIView):
    # NOTA: Esta vista parece no estar en uso - considerar eliminar
    def post(self, request):
        try:
            serializer = PedidoProductoTopicSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exceptions=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except DRFValidationError as e:
            return Response({"error" : "Exception de error de validacion", "detail": e.detail}, status=e.status_code)
        
        except IntegrityError as e:
            return Response({"error" : "Exception de error de integridad", "detail (str)" : str(e)},status=e.status_code)
        
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all().order_by("nombre_topic")
    serializer_class = TopicSerializer

@api_view(['POST']) 
def receiveOrder(request):
    """
    Procesa y guarda pedidos completos enviados desde el frontend.
    
    Esta función recibe un array de elementos de pedido desde 'tomarPedido.js',
    valida los datos, crea el pedido principal y guarda todos los productos
    y topics asociados en la base de datos.
    
    Estructura esperada de datos:
    [
        {
            "id_elemento": int,
            "precio_total": float,
            "precio_unidad_producto": float,
            "descripcion_pedido": str,
            "producto": {
                "id_producto": int,
                "cantidad_producto": int,
                "detalle_producto": str,
                "topics": [
                    {
                        "id_topic": int,
                        "cantidad_topic": int,
                        "detalle_topic": str
                    }
                ]
            }
        }
    ]
    
    Args:
        request: HttpRequest con datos del pedido en format JSON
        
    Returns:
        Response: JSON con mensaje de éxito o error detallado
        
    Raises:
        HTTP_400_BAD_REQUEST: Cuando faltan datos o son inválidos
        HTTP_404_NOT_FOUND: Cuando un producto no existe
    """
    hoy = timezone.now() #SE COLOCO ESTO PQ ANTES ESTABA .datetime() y eso no da la fecha, solo es un modulo
    data = request.data
    if not data:
        return Response({"message" : "No llegaron datos"}, status = status.HTTP_400_BAD_REQUEST)
    print(F"DATOS RECIBIDOS: {data}")

    seCreoPedido = False    
    for elemento in data:
        try:
            #EXTRACCION DE INFORMACION GENERAL DEL ELEMENTO-PEDIDO
            id_elemento = elemento["id_elemento"]
            precio_total = elemento["precio_total"]
            precio_unidad_producto = elemento["precio_unidad_producto"]
            descripcion_pedido = elemento["descripcion_pedido"]
            #EXTRACCION DEL PRODUCTO EN EL ELEMENTO
            producto = elemento["producto"]
            id_producto = producto["id_producto"]
            detalle_producto = producto["detalle_producto"]
            cantidad_producto = int(producto["cantidad_producto"])
            if cantidad_producto < 1:
                return Response({"message": "La cantidad de producto no puede ser menor a 1."}, status= status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            return Response({"message" : "Elementos invalidos o inexistentes", "detail" : str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
        if not seCreoPedido:
            try:
                pedido = Pedidos.objects.create(sub_total = precio_total, total = precio_total, estado = "Pendiente", descripcion = descripcion_pedido if descripcion_pedido else "Ninguna", fecha_pedido = hoy)
                seCreoPedido = True
            except (DataError, IntegrityError) as e:
                return Response({"message": "Error al crear el pedido.", "detail" : str(e)}, status = status.HTTP_400_BAD_REQUEST)
            
        try: 
            OBJETO_producto = Productos.objects.get(id = id_producto)
        except Productos.DoesNotExist as e:
            return Response({"message": "Producto no encontrado.", "detail": str(e)}, status= status.HTTP_404_NOT_FOUND)

        try:
            OBJETO_pedido_producto = Pedido_Producto.objects.create(fk_pedido = pedido, fk_producto = OBJETO_producto, cantidad_producto = cantidad_producto, detalle_producto = detalle_producto)
        except (IntegrityError, ValueError, DataError, TypeError) as e:
            return  Response({"message": "Error al crear el producto, puede haber un valor invalido", "detail": str(e)})
        
        for topic in producto.get("topics", []):
            try:
                id_topic = topic["id_topic"]
                OBJETO_topic = Topics.objects.get(id = id_topic)
                detalle_topic = topic["detalle_topic"]
                cantidad_topic = int(topic["cantidad_topic"])
                if cantidad_topic < 1:
                    return Response({"message": "La cantidad de topics NO debe ser menor a 1."}, status=status.HTTP_400_BAD_REQUEST)
                pedido_producto_topic = Pedido_Producto_Topic.objects.create(fk_id_pedido_producto = OBJETO_pedido_producto, fk_topic = OBJETO_topic, cantidad_topic = cantidad_topic, detalle_topic = detalle_topic)
            except (KeyError, Topics.DoesNotExist, DataError) as e:
                return Response({"message" : "Faltan datos o no existe el Topic o error al crear el Pedido_Producto_Topic", "detail" : str(e)})
            if not pedido_producto_topic:
                message = "ERROR al crear un pedido_producto_topic"
                return  Response({"message": message})
           
    message = "Todo Ok (al parecer)"
    return  Response({"message": message})

@api_view(["PUT"])
def changeDescriptionOrder(request):
    """
    Actualiza la descripción de un pedido específico.
    
    Recibe el ID del pedido y la nueva descripción desde 'ordersTaken.js'
    para permitir la edición de descripciones de pedidos existentes.
    
    Estructura de datos esperada:
    {
        "order_id": int,
        "new_description": str
    }
    
    Args:
        request: HttpRequest con order_id y new_description
        
    Returns:
        Response: JSON con mensaje de éxito o error
        
    Raises:
        HTTP_400_BAD_REQUEST: Datos faltantes o inválidos
        HTTP_404_NOT_FOUND: Pedido no encontrado
    """
    data = request.data
    if not data:
        return Response({"message": "No llegaron datos"}, status = status.HTTP_404_NOT_FOUND)
    # 1. Validación mejorada
    try:
        order_id = data["order_id"]
        new_description = data["new_description"]

    except KeyError: 
        return Response({"message": "Se pausó por falta de datos", "detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 2. Manejo de error si el pedido no existe
        pedido_object = Pedidos.objects.get(id=order_id)
    except Pedidos.DoesNotExist as e:
        return Response({"message": f"El pedido con id {order_id} no existe.", "detail" : str(e)}, status=status.HTTP_404_NOT_FOUND)

    # Lógica de actualización
    pedido_object.descripcion = new_description
    
    try:
        pedido_object.save()
        return Response(
            {"message": "La descripción se actualizó correctamente."},
            status=status.HTTP_200_OK
        )
    except (ValueError, IntegrityError, DataError)as e:
        return Response({"message": "Error en los datos que se intentaroon guardar.", "detail": str(e)}, status = status.HTTP_400_BAD_REQUEST)




class showOrdersTaken(LoginRequiredMixin, ListView):
    model = Pedidos
    context_object_name = "Pedidos"
    template_name = "ordersTaken.html"
    def get_queryset(self):
        return Pedidos.objects.filter(estado = "Pendiente").prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
    


class showAllOrders(LoginRequiredMixin, ListView):
    """
    Vista para mostrar pedidos filtrados por fecha.
    Utiliza timezone de Colombia para fechas locales.
    """
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


@login_required
def cancelarPedido(request, id):
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Cancelado"
    pedido.save()
    return redirect("showOrdersTaken")

@login_required
def pagarPedido(request, id):
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Pagado"
    pedido.save()
    return redirect("showOrdersTaken")
    




class adminProductos(LoginRequiredMixin, ListView):
    model = Productos
    template_name = "adminProductos.html"
    # context_object_name = "Objetos_productos"

class crearProducto(LoginRequiredMixin, CreateView):
    model = Productos
    template_name="formularioCrearProducto.html"
    success_url = reverse_lazy("adminProductos")
    form_class = forms.FormularioEditarProducto

class editarProducto(LoginRequiredMixin, UpdateView):
    model = Productos
    form_class = forms.FormularioEditarProducto
    success_url = reverse_lazy("adminProductos")
    template_name = "formularioEditarProducto.html"

class eliminarProducto(LoginRequiredMixin, DeleteView):
    model = Productos
    template_name = "confirmDeleteProducto.html"
    success_url= reverse_lazy("adminProductos")
    context_object_name = "Producto"

@login_required
def deshabilitarProducto(request, id):
    producto_id = id
    objetoProducto = Productos.objects.get(id = id)
    objetoProducto.estado_producto = "Deshabilitado"
    objetoProducto.save()
    return redirect("adminProductos")

@login_required
def activarProducto(request, id):
    # TODO: Corregir redirección - debería ir a adminProductos
    objectoProducto = Productos.objects.get(id = id)
    objectoProducto.estado_producto = "Activo"
    objectoProducto.save()
    return redirect("adminTopics")




class adminTopics(LoginRequiredMixin, ListView):
    model = Topics
    template_name = "adminTopics.html"
    # context_object_name = "ObjetoTopics"

class crearTopic(LoginRequiredMixin, CreateView):
    model = Topics
    template_name = "formularioCrearTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic

class editarTopic(LoginRequiredMixin, UpdateView):
    model = Topics
    template_name = "formularioEditarTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic

class eliminarTopic(LoginRequiredMixin, DeleteView):
    model = Topics
    template_name = "confirmDeleteTopic.html"
    success_url = reverse_lazy("adminTopics")
    context_object_name = "Topic"

@login_required
def deshabilitarTopic(request, id):
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Deshabilitado"
    objectoTopic.save()
    return redirect("adminTopics")

@login_required
def activarTopic(request, id):
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Activo"
    objectoTopic.save()
    return redirect("adminTopics")
