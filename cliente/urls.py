from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
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
    path('logout/', views.logout_view, name='logout'),
    path('agregar-al-carrito/<int:product_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('disminuir_cantidad/<int:cart_item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('aumentar_cantidad/<int:cart_item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('realizar_compra', views.realizar_compra, name='realizar_compra'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('perfil/', views.perfil, name='perfil'),
    path('editaruser/<id>/', views.editar_usuario,name="editar_usuario"),
    path('eliminaruser/<id>/',views.eliminar_usuario,name="eliminar_usuario"),
    # ...
]
