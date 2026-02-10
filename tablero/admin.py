from django.contrib import admin

# Register your models here.from django.contrib import admin
from .models import Marca, Producto, Descuento

class DescuentoInline(admin.TabularInline):
    model = Descuento
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "marca",
        "precio_origen_ars",
        "total_descuento_porcentual",
        "precio_final_ars",
        "activo",
    )
    list_filter = ('marca', 'activo')
    search_fields = ('nombre',)
    inlines = [DescuentoInline]

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
