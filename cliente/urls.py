from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('', views.home, name='home'),
    path('hombre/', views.hombre, name='hombre'),
    path('mujeres/', views.mujeres, name='mujeres'),
    path('sale/', views.sale, name='sale'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('productos/', views.listarproductos, name='listar_productos'),
    path('editarprod/<id>/', views.editar_producto,name="editar_producto"),
    path('eliminarprod/<id>/',views.eliminar_producto,name="eliminar_producto"),
]
