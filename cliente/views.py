
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

def home(request):
    return render(request, 'Home.html')

def hombre(request):
    return render(request, 'products.html')

def mujeres(request):
    return render(request, 'products-mujer.html')

def sale(request):
    return render(request, 'sales.html')

def register(request):
    # Lógica para el registro de usuarios
    if request.method == 'POST':
        # Procesar el formulario de registro
        # Crear el nuevo usuario y guardar en la base de datos
        return redirect('login')
    else:
        # Mostrar el formulario de registro
        return render(request, 'registro.html')

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

def login(request):
    # Lógica para el inicio de sesión de usuarios
    if request.method == 'POST':
        # Procesar el formulario de inicio de sesión
        # Verificar las credenciales del usuario
        return redirect('dashboard')
    else:
        # Mostrar el formulario de inicio de sesión
        return render(request, 'login.html')

@login_required
def dashboard(request):
    # Lógica para la página de inicio (dashboard) del usuario logueado
    # Obtener los productos disponibles
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    # Lógica para agregar un producto al carrito de compras
    product = Product.objects.get(pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    # Lógica para mostrar el carrito de compras del usuario
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'carro.html', {'cart_items': cart_items})
