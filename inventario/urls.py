from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('registro/', views.registro),
    path('login/', views.login),

    # Categorias
    path('categorias/', views.listar_categorias),
    path('categorias/crear/', views.crear_categoria),

    # Productos
    path('productos/', views.listar_productos),
    path('productos/crear/', views.crear_producto),
    path('productos/<int:id>/', views.obtener_producto),
    path('productos/<int:id>/actualizar/', views.actualizar_producto),
    path('productos/<int:id>/eliminar/', views.eliminar_producto),

    # Movimientos
    path('movimientos/', views.listar_movimientos),
    path('movimientos/crear/', views.crear_movimiento),
]