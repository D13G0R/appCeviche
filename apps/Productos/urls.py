from apps.Productos import views

from django.urls import path
from .views import PedidoProductoTopicView

urlpatterns = [
    path('takeOrders/', views.view_take_order.as_view(), name = 'takeOrderView'),
    path('showAllOrders/', views.showAllOrders.as_view(), name='AllOrders'),  # sin parámetro
    path('showAllOrdersDay/<int:dia>', views.showAllOrders.as_view(), name='AllOrdersForDay'),  # con día
    path('pedido-producto-topic/', PedidoProductoTopicView.as_view(), name='pedido_producto_topic'),
    path('showOrdersTaken/', views.showOrdersTaken.as_view(), name = "showOrdersTaken"),
    path('cancelarPedido/<int:id>', views.cancelarPedido, name = "cancelarPedido"),
    path('pagarPedido/<int:id>', views.pagarPedido, name = "pagarPedido"),
    # path("filtarFecha/", views.filtrarFecha, name = "filtrarFecha"),
    # path("filtarFecha/<int:pk>", views.filtrarFecha, name = "filtrarFecha"),

    path('showProductos/', views.adminProductos.as_view(), name = "adminProductos"),
    path('editarProducto/<int:pk>', views.editarProducto.as_view(), name = "editarProducto"),
    path('eliminarProducto/<int:pk>', views.eliminarProducto.as_view(), name = "eliminarProducto"),
    path('crearProducto/', views.crearProducto.as_view(), name = "crearProducto"),
    path('deshabilitarProducto/<int:id>', views.deshabilitarProducto, name = "deshabilitarProducto"),
    path('activarProducto/<int:id>', views.activarProducto, name = "activarProducto"),

    path('showTopics/', views.adminTopics.as_view(), name = "adminTopics"),
    path('editarTopic/<int:pk>', views.editarTopic.as_view(), name = "editarTopic"),
    path('eliminarTopic/<int:pk>', views.eliminarTopic.as_view(), name = "eliminarTopic"),
    path('crearTopic/', views.crearTopic.as_view(), name = "crearTopic"),
    path('deshabilitarTopic/<int:id>', views.deshabilitarTopic, name = "deshabilitarTopic"),
    path('activarTopic/<int:id>', views.activarTopic, name = "activarTopic")
]

