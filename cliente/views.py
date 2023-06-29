
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Product, Cart, CartItem



def home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'Home.html', context)

def hombre(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products.html', context)

def mujeres(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'products-mujer.html', context)

def calculate_discounted_price(price, discount_percentage):
    discounted_price = price * (1 - discount_percentage/100)
    return discounted_price


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
        User.objects.create_user(username=username, password=password, email=email)

        return JsonResponse({'mensaje': 'Registrado con éxito'})

    return render(request, 'registro.html')


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Product, id=producto_id)
    return render(request, 'view-product.html', {'product': producto})


def login(request):
    # Lógica para el inicio de sesión de usuarios
    if request.method == 'POST':
        # Procesar el formulario de inicio de sesión
        # Verificar las credenciales del usuario
        return redirect('dashboard')
    else:
        # Mostrar el formulario de inicio de sesión
        return render(request, 'login.html')


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

