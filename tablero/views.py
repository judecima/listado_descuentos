from django.shortcuts import render
from .models import Producto

def listado_productos(request):
    productos = Producto.objects.filter(activo=True).prefetch_related('descuentos', 'marca')
    return render(request, 'tablero/listado_productos.html', {
        'productos': productos
    })
