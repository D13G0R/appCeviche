from apps.Productos import views

from django.urls import path
from .views import PedidoProductoTopicView

urlpatterns = [
    path('takeOrders/', views.view_take_order.as_view(), name = 'takeOrderView'),
    path('pedido-producto-topic/', PedidoProductoTopicView.as_view(), name='pedido_producto_topic'),
    path('showOrdersTaken/', views.showOrdersTaken.as_view(), name = "showOrdersTaken"),
    path('cancelarPedido/<int:id>', views.cancelarPedido, name = "cancelarPedido"),
    path('pagarPedido/<int:id>', views.pagarPedido, name = "pagarPedido"),

    path('showProductos/', views.showAllProducts.as_view(), name = "adminProductos"),
    path('editarProducto/<int:pk>', views.editarProducto.as_view(), name = "editarProducto"),
    path('eliminarProducto/<int:pk>', views.eliminarProducto.as_view(), name = "eliminarProducto"),
    path('crearProducto/', views.crearProducto.as_view(), name = "crearProducto"),
    path('deshabilitarProducto/<int:id>', views.deshabilitarProducto, name = "deshabilitarProducto")
]

