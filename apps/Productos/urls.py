from apps.Productos import views
from django.urls import path
from django.urls import path
from .views import PedidoProductoTopicView

urlpatterns = [
    path("takeOrders/", views.view_take_order.as_view(), name = "takeOrderView"),
    path('pedido-producto-topic/', PedidoProductoTopicView.as_view(), name='pedido_producto_topic'),
]

