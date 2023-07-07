from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group, Permission
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Purchase, PurchaseItem
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.db import transaction




def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'Home.html', context)

@login_required
def hombre(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products.html', context)

@login_required
def mujeres(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products-mujer.html', context)


def calculate_discounted_price(price, discount_percentage):
    discounted_price = price * (1 - discount_percentage/100)
    return discounted_price

@login_required
def sale(request):
    products = Product.objects.all()
    discount_percentage = 20  # Porcentaje de descuento (ajústalo según sea necesario)

    # Calcular el precio descontado para cada producto
    for product in products:
        product.discounted_price = calculate_discounted_price(product.price, discount_percentage)

    context = {
        'products': products,
    }

    return render(request, 'sales.html', context)

@user_passes_test(lambda user: user.is_superuser)
def listarproductos(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'listado-productos.html', context)


def editar_producto(request, id):
    product = get_object_or_404(Product,id=id)
    if request.method == 'POST':
        # Obtén los datos del formulario
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        marca = request.POST['marca']
        descripcion = request.POST['descripcion']
        size = request.POST['size']
        gender = request.POST['gender']
        model = request.POST['model']
        # Otros campos del formulario

        # Actualiza los datos del producto
        product.name = nombre
        product.price = precio
        product.brand = marca
        product.description = descripcion
        product.size = size
        product.gender = gender
        product.model = model
        # Otros campos del producto

        # Guarda los cambios en la base de datos
        product.save()

        # Redirige a la página de listado de productos
        return redirect(to = 'listar_productos')
    return redirect(to="login")

    
@user_passes_test(lambda user: user.is_superuser)
def eliminar_producto(request, id):
    product = get_object_or_404(Product,id=id)
    product.delete()
    return redirect(to="listar_productos")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        # Validar los campos
        errores = []

        if not username.strip() or len(username) < 3:
            errores.append("Formato no válido para el nombre, solo letras y mínimo 3 caracteres")

        if not password.strip() or len(password) < 10:
            errores.append("Formato no válido para la contraseña, mínimo 10 caracteres")

        if not email.strip() or '@' not in email:
            errores.append("Escriba un correo válido")

        if errores:
            return JsonResponse({'errores': errores}, status=400)

        # Verificar si el usuario ya existe en la base de datos
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            return JsonResponse({'errores': ['El usuario ya existe']}, status=400)

        # Crear el nuevo usuario y guardar en la base de datos
        user = User.objects.create_user(username=username, password=password, email=email)

        # Obtener el permiso "can view product"
        content_type = ContentType.objects.get(app_label='cliente', model='product')
        permission = Permission.objects.get(content_type=content_type, codename='view_product')

        # Agregar el permiso al usuario
        user.user_permissions.add(permission)

        return JsonResponse({'mensaje': 'Registrado con éxito'})

    return render(request, 'registro.html')

@login_required
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    return render(request, 'view-product.html', {'product': producto})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Iniciar sesión
            login(request, user)
            return JsonResponse({'mensaje': 'Inició sesión con éxito'}) 
        else:
            return JsonResponse({'errores': ['Credenciales inválidas']}, status=400)

    return render(request, 'login.html')
@user_passes_test(lambda user: user.is_superuser)
def dashboard(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        precio = request.POST['precio']
        marca = request.POST['marca']
        descripcion = request.POST['descripcion']
        print(request.FILES)  # A
        imagen = request.FILES['imagen']
        size = request.POST['size']
        gender = request.POST['gender']
        model = request.POST['model']
        
        # Validar los campos
        errores = []
        
        if not nombre.strip() or len(nombre) < 3:
            errores.append("Formato no válido para el nombre, solo letras y mínimo 3 caracteres")

        if not precio.strip() or int(precio) < 1000:
            errores.append("Formato no válido para el precio, debe ser un número mayor o igual a 1000")

        if not marca.strip():
            errores.append("Debe seleccionar una marca")

        if not descripcion.strip():
            errores.append("La descripción del producto es requerida")

        if not size.strip():
            errores.append("El campo de la talla de zapatilla es requerido")

        if not gender.strip():
            errores.append("Debe seleccionar el género del producto")

        if not model.strip():
            errores.append("El campo de modelo es requerido")

        if errores:
            return JsonResponse({'errores': errores}, status=400)
        
        # Crea el nuevo producto y guárdalo en la base de datos
        Product.objects.create(name=nombre, price=precio, brand=marca, description=descripcion,
                        image=imagen, size=size, gender=gender, model=model)

        
        return JsonResponse({'mensaje': 'Producto cargado con éxito'})
    
    return render(request, 'admin.html')

def logout_view(request):
    logout(request)
    return redirect(to='login')   

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

@login_required
def agregar_al_carrito(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('carrito')
@login_required
def carrito(request):
    cart = Cart.objects.filter(user=request.user).first()
    total = cart.total if cart else 0
    cart_items = cart.cartitem_set.select_related('product') if cart else []

    

    context = {
        'cart': cart_items,
        'total': total,
        'cart_id': cart.id, 
    }

    return render(request, 'carro.html', context)

@login_required
def disminuir_cantidad(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif cart_item.quantity == 1:
        cart_item.delete()
    
    return redirect('carrito')

@login_required
def aumentar_cantidad(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    
    if cart_item.quantity < 15:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('carrito')

def realizar_compra(request):
    # Obtener el usuario actual y su carrito
    user = request.user
    cart = get_object_or_404(Cart, user=user)

    # Calcular el total del carrito
    total = cart.total
    

    with transaction.atomic():
        # Restar el stock de cada producto en el carrito
        for item in cart.cartitem_set.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
            

        # Crear la instancia de la compra
        purchase = Purchase.objects.create(user=user, cart=cart, total=total)

        for item in cart.cartitem_set.all():
            product = item.product
            purchase_item = PurchaseItem.objects.create(purchase=purchase, product=product, quantity=item.quantity)

        # Reiniciar el carrito
        cart.products.clear()

    # Redirigir a una página de confirmación o a donde desees
    return redirect('home')  # Ajusta la URL según tu configuración

def ordenes(request):
    user = request.user
    pedidos = Purchase.objects.filter(user=user)

    context = {
        'pedidos': pedidos
    }

    return render(request, 'ordenes.html', context)



@login_required
def editar_usuario(request, id):
    # Obtener el usuario que se desea editar
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        # Obtener los datos enviados en el formulario
        username = request.POST['username']
        email = request.POST['email']
        # Otros campos que deseas editar

        # Actualizar los campos del usuario
        user.username = username
        user.email = email
        # Actualizar otros campos si es necesario

        # Guardar los cambios en la base de datos
        user.save()

        # Redirigir a una página de éxito o a donde desees
        return redirect(to = 'perfil')  # Ajusta la URL según tu configuración
    return redirect( to="home" )


@login_required
def eliminar_usuario(request, id):
    # Obtener el usuario que se desea eliminar
    user = get_object_or_404(User, id=id)
    if user:

        # Eliminar el usuario
        user.delete()

        # Redirigir a una página de éxito o a donde desees
        return redirect( to ='login')  # Ajusta la URL según tu 
    return redirect( to="perfil" )

def perfil(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'perfil.html', context)

