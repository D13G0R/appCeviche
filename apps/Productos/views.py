# Django imports
import logging
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError, DataError
from datetime import datetime, time
import pytz

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

logger = logging.getLogger(__name__)

class view_take_order(LoginRequiredMixin, ListView):
    """
    Vista para tomar pedidos.

    Muestra los productos ya registrados en la base de datos junto con los topics que tambien han sido cargados

    Attributes:
        model(Model): modelo productos para traer los datos;
        context_object_name(str): no quiero que se llame simplemente object_list, asi que le puse de nombre 'Productos';
        template_name(str): plantilla en la que cargará todo;

    Methods:
        get_context_data(self, *, object_list=None, **kwargs): Agrega al contexto la lista de topics que estan en la base de datos ordenados por nombre;
    """
    model = Productos
    context_object_name = "Productos"
    template_name = "tomarPedido.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        logger.info("Accediendo a la vista de tomar pedido.")
        context = super().get_context_data(**kwargs)
        context["Topics"] = Topics.objects.all().order_by("nombre_topic")
        return context

class PedidoProductoTopicView(APIView):
    # NOTA: Esta vista parece no estar en uso - considerar eliminar
    def post(self, request):
        logger.info("Recibiendo solicitud en PedidoProductoTopicView.")
        try:
            serializer = PedidoProductoTopicSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exceptions=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except DRFValidationError as e:
            logger.error(f"Error de validación en PedidoProductoTopicView: {str(e)}")
            return Response({"error" : "Exception de error de validacion", "detail": e.detail}, status=e.status_code)
        
        except IntegrityError as e:
            logger.error(f"Error de integridad en PedidoProductoTopicView: {str(e)}")
            return Response({"error" : "Exception de error de integridad", "detail (str)" : str(e)},status=e.status_code)
        
    

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topics.objects.all().order_by("nombre_topic")
    serializer_class = TopicSerializer

    def list(self, request, *args, **kwargs):
        logger.info("Listando topics vía API.")
        return super().list(request, *args, **kwargs)

@api_view(['POST']) 
def receiveOrder(request):
    """
    Procesa y guarda pedidos completos enviados desde el frontend.
    """
    logger.info("Recibiendo solicitud para crear un nuevo pedido.")
    hoy = timezone.now() 
    data = request.data

    if not data:
        logger.warning("Solicitud de pedido recibida sin datos.")
        return Response({"message" : "No llegaron datos"}, status = status.HTTP_400_BAD_REQUEST)
    
    logger.debug(f"Datos recibidos: {data}")
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
                logger.error(f"Cantidad de producto inválida: {cantidad_producto}")
                return Response({"message": "La cantidad de producto no puede ser menor a 1."}, status= status.HTTP_400_BAD_REQUEST)

        except KeyError as e:
            logger.error(f"Error de clave en los datos recibidos: {str(e)}")
            return Response({"message" : "Elementos invalidos o inexistentes", "detail" : str(e)}, status = status.HTTP_400_BAD_REQUEST)
        
        if not seCreoPedido:
            try:
                pedido = Pedidos.objects.create(sub_total = precio_total, total = precio_total, estado = "Pendiente", descripcion = descripcion_pedido if descripcion_pedido else "Ninguna", fecha_pedido = hoy)
                seCreoPedido = True
                logger.info(f"Pedido principal creado exitosamente. ID: {pedido.id}")
            except (DataError, IntegrityError) as e:
                logger.error(f"Error al crear el pedido principal: {str(e)}")
                return Response({"message": "Error al crear el pedido.", "detail" : str(e)}, status = status.HTTP_400_BAD_REQUEST)
            
        try: 
            OBJETO_producto = Productos.objects.get(id = id_producto)

            OBJETO_pedido_producto = Pedido_Producto.objects.create(fk_pedido = pedido, fk_producto = OBJETO_producto, cantidad_producto = cantidad_producto, detalle_producto = detalle_producto)
            logger.info(f"Producto {id_producto} agregado al pedido {pedido.id}.")
        
        except Productos.DoesNotExist as e:
            logger.error(f"Producto {id_producto} no encontrado.")
            return Response({"message": "Producto no encontrado.", "detail": str(e)}, status= status.HTTP_404_NOT_FOUND)
        
        except (IntegrityError, ValueError, DataError, TypeError) as e:
            logger.error(f"Error al asociar producto {id_producto} al pedido: {str(e)}")
            return  Response({"message": "Error al crear el producto, puede haber un valor invalido", "detail": str(e)})
        
        for topic in producto.get("topics", []):

            try:
                id_topic = topic["id_topic"]
                OBJETO_topic = Topics.objects.get(id = id_topic)
                detalle_topic = topic["detalle_topic"]
                cantidad_topic = int(topic["cantidad_topic"])

                if cantidad_topic < 1:
                    logger.error(f"Cantidad de topic inválida: {cantidad_topic}")
                    return Response({"message": "La cantidad de topics NO debe ser menor a 1."}, status=status.HTTP_400_BAD_REQUEST)
                
                pedido_producto_topic = Pedido_Producto_Topic.objects.create(fk_id_pedido_producto = OBJETO_pedido_producto, fk_topic = OBJETO_topic, cantidad_topic = cantidad_topic, detalle_topic = detalle_topic)
                logger.info(f"Topic {id_topic} agregado al producto {id_producto} del pedido {pedido.id}.")

            except (KeyError, Topics.DoesNotExist, DataError) as e:
                logger.error(f"Error al procesar topic para el producto {id_producto}: {str(e)}")
                return Response({"message" : "Faltan datos o no existe el Topic o error al crear el Pedido_Producto_Topic", "detail" : str(e)})
            
            if not pedido_producto_topic:
                logger.error("Fallo la creación del objeto Pedido_Producto_Topic.")
                message = "ERROR al crear un pedido_producto_topic"
                return  Response({"message": message})
           
    logger.info(f"Pedido {pedido.id} completado satisfactoriamente.")
    message = "Pedido creado satisfactoriamente"
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
    logger.info("Solicitud para cambiar la descripción de un pedido.")
    data = request.data
    if not data:
        return Response({"message": "No llegaron datos"}, status = status.HTTP_404_NOT_FOUND)
    # 1. Validación mejorada
    try:
        order_id = data["order_id"]
        new_description = data["new_description"]

    except KeyError as e: 
        logger.error(f"Faltan datos para cambiar la descripción: {str(e)}")
        return Response({"message": "Se pausó por falta de datos", "detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 2. Manejo de error si el pedido no existe
        pedido_object = Pedidos.objects.get(id=order_id)
    except Pedidos.DoesNotExist as e:
        logger.warning(f"Intento de cambiar descripción de pedido inexistente: {order_id}")
        return Response({"message": f"El pedido con id {order_id} no existe.", "detail" : str(e)}, status=status.HTTP_404_NOT_FOUND)

    # Lógica de actualización
    pedido_object.descripcion = new_description
    
    try:
        pedido_object.save()
        logger.info(f"Descripción del pedido {order_id} actualizada correctamente.")
        return Response(
            {"message": "La descripción se actualizó correctamente."},
            status=status.HTTP_200_OK
        )
    except (ValueError, IntegrityError, DataError)as e:
        logger.error(f"Error al guardar la nueva descripción del pedido {order_id}: {str(e)}")
        return Response({"message": "Error en los datos que se intentaroon guardar.", "detail": str(e)}, status = status.HTTP_400_BAD_REQUEST)




class showOrdersTaken(LoginRequiredMixin, ListView):
    """
    Mostrar ordenes ya tomadas pero antes de ser pagadas.

    Muestra todos los pedidos con su productos y topics asociados.

    Attributes:
        model(Model): modelo productos para traer los datos.
        context_object_name(str): no quiero que se llame simplemente object_list, asi que le puse de nombre 'Productos'.
        template_name(str): plantilla en la que cargará todo.
    Methods:
        get_queryset(self): Para mostrar todos los pedidos que están aun por pagar.
    """
    model = Pedidos
    context_object_name = "Pedidos"
    template_name = "ordersTaken.html"
    def get_queryset(self):
        logger.info("Mostrando órdenes tomadas (pendientes).")
        return Pedidos.objects.filter(estado = "Pendiente").prefetch_related("detalle_pedido__topics_de_producto__fk_topic")
    


class showAllOrders(LoginRequiredMixin, ListView):
    """
    Vista para mostrar pedidos pagados.
    Por defecto muestra todos los pedidos pagados.
    Utiliza timezone de Colombia para fechas locales.
    """
    model = Pedidos
    context_object_name = "Pedidos"
    template_name = "allOrders.html"
    hoy = timezone.localtime(timezone.now())
    dia_seleccionado = ""

    def get_queryset(self):
        logger.info("Accediendo a la vista de todos los pedidos pagados.")
        dia_str = self.kwargs.get("dia")
        if dia_str:
            try:
                fecha_str = dia_str  # "YYYY-MM-DD"
                fecha_date = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                self.dia_seleccionado = fecha_date
                
                # Crear rango de fechas respetando el timezone local
                bogota_tz = pytz.timezone('America/Bogota')
                fecha_inicio_local = bogota_tz.localize(datetime.combine(fecha_date, time.min))
                fecha_fin_local = bogota_tz.localize(datetime.combine(fecha_date, time.max))
                
                # Convertir a UTC para la consulta
                fecha_inicio_utc = fecha_inicio_local.astimezone(pytz.UTC)
                fecha_fin_utc = fecha_fin_local.astimezone(pytz.UTC)
                
                # Filtrar por rango de fechas y solo pedidos pagados
                return Pedidos.objects.filter(
                    fecha_pedido__gte=fecha_inicio_utc, 
                    fecha_pedido__lte=fecha_fin_utc,
                    estado="Pagado"
                ).prefetch_related("detalle_pedido__topics_de_producto__fk_topic").order_by('-fecha_pedido')
                
            except ValueError:
                # Fecha inválida, mostrar todos los pedidos pagados
                self.dia_seleccionado = "Fecha inválida - Mostrando todos"
                return Pedidos.objects.filter(estado="Pagado").prefetch_related("detalle_pedido__topics_de_producto__fk_topic").order_by('-fecha_pedido')
        else:
            # Sin parámetro, mostrar TODOS los pedidos pagados (no solo los de hoy)
            self.dia_seleccionado = "Todas las fechas"
            return Pedidos.objects.filter(estado="Pagado").prefetch_related("detalle_pedido__topics_de_producto__fk_topic").order_by('-fecha_pedido')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hoy"] = self.dia_seleccionado
        return context
    

@login_required
def cancelarPedido(request, id):
    logger.info(f"Cancelando pedido con ID: {id}")
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Cancelado"
    pedido.save()
    return redirect("showOrdersTaken")

@login_required
def pagarPedido(request, id):
    logger.info(f"Pagando pedido con ID: {id}")
    pedido = Pedidos.objects.get(id = id)
    pedido.estado = "Pagado"
    pedido.save()
    return redirect("showOrdersTaken")
    




class adminProductos(LoginRequiredMixin, ListView):
    model = Productos
    template_name = "adminProductos.html"
    def get(self, request, *args, **kwargs):
        logger.info("Accediendo a la vista de administración de productos.")
        return super().get(request, *args, **kwargs)

class crearProducto(LoginRequiredMixin, CreateView):
    model = Productos
    template_name="formularioCrearProducto.html"
    success_url = reverse_lazy("adminProductos")
    form_class = forms.FormularioEditarProducto
    def dispatch(self, request, *args, **kwargs):
        logger.info("Accediendo a la creación de producto.")
        return super().dispatch(request, *args, **kwargs)

class editarProducto(LoginRequiredMixin, UpdateView):
    model = Productos
    form_class = forms.FormularioEditarProducto
    success_url = reverse_lazy("adminProductos")
    template_name = "formularioEditarProducto.html"
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Editando producto ID: {self.kwargs.get('pk')}")
        return super().dispatch(request, *args, **kwargs)

class eliminarProducto(LoginRequiredMixin, DeleteView):
    model = Productos
    template_name = "confirmDeleteProducto.html"
    success_url= reverse_lazy("adminProductos")
    context_object_name = "Producto"
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Eliminando producto ID: {self.kwargs.get('pk')}")
        return super().dispatch(request, *args, **kwargs)

@login_required
def deshabilitarProducto(request, id):
    logger.info(f"Deshabilitando producto con ID: {id}")
    objetoProducto = Productos.objects.get(id = id)
    objetoProducto.estado_producto = "Deshabilitado"
    objetoProducto.save()
    return redirect("adminProductos")

@login_required
def activarProducto(request, id):
    logger.info(f"Activando producto con ID: {id}")
    # TODO: Corregir redirección - debería ir a adminProductos
    objectoProducto = Productos.objects.get(id = id)
    objectoProducto.estado_producto = "Activo"
    objectoProducto.save()
    return redirect("adminProductos")




class adminTopics(LoginRequiredMixin, ListView):
    model = Topics
    template_name = "adminTopics.html"
    def get(self, request, *args, **kwargs):
        logger.info("Accediendo a la vista de administración de topics.")
        return super().get(request, *args, **kwargs)

class crearTopic(LoginRequiredMixin, CreateView):
    model = Topics
    template_name = "formularioCrearTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic
    def dispatch(self, request, *args, **kwargs):
        logger.info("Creando nuevo topic.")
        return super().dispatch(request, *args, **kwargs)

class editarTopic(LoginRequiredMixin, UpdateView):
    model = Topics
    template_name = "formularioEditarTopic.html"
    success_url = reverse_lazy("adminTopics")
    form_class = forms.FormularioEditarTopic
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Editando topic ID: {self.kwargs.get('pk')}")
        return super().dispatch(request, *args, **kwargs)

class eliminarTopic(LoginRequiredMixin, DeleteView):
    model = Topics
    template_name = "confirmDeleteTopic.html"
    success_url = reverse_lazy("adminTopics")
    context_object_name = "Topic"
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Eliminando topic ID: {self.kwargs.get('pk')}")
        return super().dispatch(request, *args, **kwargs)

@login_required
def deshabilitarTopic(request, id):
    logger.info(f"Deshabilitando topic con ID: {id}")
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Deshabilitado"
    objectoTopic.save()
    return redirect("adminTopics")

@login_required
def activarTopic(request, id):
    logger.info(f"Activando topic con ID: {id}")
    objectoTopic = Topics.objects.get(id = id)
    objectoTopic.estado_topic = "Activo"
    objectoTopic.save()
    return redirect("adminTopics")
