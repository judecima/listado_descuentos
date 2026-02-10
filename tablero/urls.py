from django.urls import path
from .views import listado_productos

app_name = "tablero"

urlpatterns = [
    path('', listado_productos, name='listado'),
]
