from django.shortcuts import render
from django.views.generic import View, ListView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Pedido_Producto_Topic
from .serializers import PedidoProductoTopicSerializer
from .models import Pedidos, Productos, Topics

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