from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Categoria, Producto, Movimiento

# =========================
# AUTH
# =========================
@api_view(['POST'])
def registro(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe'}, status=400)
    user = User.objects.create_user(username=username, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=201)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Credenciales incorrectas'}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

# =========================
# CATEGORIAS
# =========================
@api_view(['GET'])
def listar_categorias(request):
    categorias = Categoria.objects.all()
    data = list(categorias.values('id', 'nombre', 'descripcion'))
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_categoria(request):
    nombre = request.data.get('nombre', '').strip()
    if not nombre:
        return Response({'error': 'El nombre es obligatorio'}, status=400)
    categoria = Categoria.objects.create(
        nombre=nombre,
        descripcion=request.data.get('descripcion', '')
    )
    return Response({'id': categoria.id, 'mensaje': 'Categoría creada'}, status=201)

# =========================
# PRODUCTOS
# =========================
@api_view(['GET'])
def listar_productos(request):
    productos = Producto.objects.all()
    data = list(productos.values('id', 'nombre', 'precio', 'stock', 'categoria__nombre'))
    return Response(data)

@api_view(['GET'])
def obtener_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    return Response({
        'id': producto.id,
        'nombre': producto.nombre,
        'descripcion': producto.descripcion,
        'precio': str(producto.precio),
        'stock': producto.stock,
        'categoria': producto.categoria.nombre if producto.categoria else None
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_producto(request):
    nombre = request.data.get('nombre', '').strip()
    precio = request.data.get('precio')
    stock = request.data.get('stock', 0)
    descripcion = request.data.get('descripcion', '')
    categoria_id = request.data.get('categoria_id', None)

    errores = {}

    if not nombre:
        errores['nombre'] = 'El nombre es obligatorio'
    if precio is None:
        errores['precio'] = 'El precio es obligatorio'
    elif float(precio) <= 0:
        errores['precio'] = 'El precio debe ser mayor a 0'
    if int(stock) < 0:
        errores['stock'] = 'El stock no puede ser negativo'
    if categoria_id and not Categoria.objects.filter(id=categoria_id).exists():
        errores['categoria_id'] = 'La categoría no existe'

    if errores:
        return Response({'errores': errores}, status=400)

    producto = Producto.objects.create(
        nombre=nombre,
        precio=precio,
        stock=stock,
        descripcion=descripcion,
        categoria_id=categoria_id,
        creado_por=request.user
    )
    return Response({'id': producto.id, 'mensaje': 'Producto creado'}, status=201)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def actualizar_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    producto.nombre = request.data.get('nombre', producto.nombre)
    producto.precio = request.data.get('precio', producto.precio)
    producto.stock = request.data.get('stock', producto.stock)
    producto.save()
    return Response({'mensaje': 'Producto actualizado'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def eliminar_producto(request, id):
    try:
        producto = Producto.objects.get(id=id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)
    producto.delete()
    return Response({'mensaje': 'Producto eliminado'})

# =========================
# MOVIMIENTOS
# =========================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_movimientos(request):
    movimientos = Movimiento.objects.all()
    data = list(movimientos.values('id', 'tipo', 'cantidad', 'fecha', 'producto__nombre', 'nota'))
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_movimiento(request):
    producto_id = request.data.get('producto_id')
    tipo = request.data.get('tipo')
    cantidad = request.data.get('cantidad')
    nota = request.data.get('nota', '')

    errores = {}

    if not producto_id:
        errores['producto_id'] = 'El producto es obligatorio'
    if tipo not in ['entrada', 'salida']:
        errores['tipo'] = 'El tipo debe ser entrada o salida'
    if not cantidad or int(cantidad) <= 0:
        errores['cantidad'] = 'La cantidad debe ser mayor a 0'

    if errores:
        return Response({'errores': errores}, status=400)

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=404)

    if tipo == 'salida' and producto.stock < int(cantidad):
        return Response({'error': 'Stock insuficiente'}, status=400)

    if tipo == 'entrada':
        producto.stock += int(cantidad)
    elif tipo == 'salida':
        producto.stock -= int(cantidad)

    producto.save()

    movimiento = Movimiento.objects.create(
        producto=producto,
        tipo=tipo,
        cantidad=cantidad,
        usuario=request.user,
        nota=nota
    )
    return Response({
        'id': movimiento.id,
        'mensaje': f'Movimiento de {tipo} registrado',
        'stock_actual': producto.stock
    }, status=201)