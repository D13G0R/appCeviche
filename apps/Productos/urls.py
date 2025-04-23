from apps.Productos import views
from django.urls import path
from django.urls import path
from .views import PedidoProductoTopicView

urlpatterns = [
    path('takeOrders/', views.view_take_order.as_view(), name = 'takeOrderView'),
    path('pedido-producto-topic/', PedidoProductoTopicView.as_view(), name='pedido_producto_topic'),
    path('showOrdersTaken/', views.showOrdersTaken.as_view(), name = "showOrdersTaken"),
    path('cancelarPedido/<int:id>', views.cancelarPedido, name = "cancelarPedido"),
    path('pagarPedido/<int:id>', views.pagarPedido, name = "pagarPedido")
]

