from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Marca(models.Model):
    nombre = models.CharField("Nombre de la marca", max_length=100, unique=True)

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField("Nombre del producto", max_length=200)
    marca = models.ForeignKey(
        Marca,
        verbose_name="Marca",
        on_delete=models.PROTECT
    )
    precio_origen = models.DecimalField(
        "Precio original",
        max_digits=10,
        decimal_places=2
    )
    activo = models.BooleanField("Activo", default=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

    # ------------------------
    # DESCUENTOS
    # ------------------------
    @property
    def total_descuento_porcentual(self):
        total = sum(d.valor for d in self.descuentos.all())
        return min(total, 100)

    # ------------------------
    # PRECIO FINAL (Decimal)
    # ------------------------
    @property
    def precio_final(self):
        descuento = Decimal(self.total_descuento_porcentual) / Decimal("100")
        return (
            self.precio_origen * (Decimal("1") - descuento)
        ).quantize(Decimal("0.00"))

    # ------------------------
    # FORMATO $ ARGENTINO
    # ------------------------
    def precio_origen_ars(self):
        return f"$ {self.precio_origen:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def precio_final_ars(self):
        return f"$ {self.precio_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    precio_origen_ars.short_description = "Precio original"
    precio_final_ars.short_description = "Precio final"


class Descuento(models.Model):
    producto = models.ForeignKey(
        Producto,
        related_name="descuentos",
        on_delete=models.CASCADE,
        verbose_name="Producto"
    )
    descripcion = models.CharField("Descripción", max_length=200)
    valor = models.PositiveIntegerField(
        "Descuento (%)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        verbose_name = "Descuento"
        verbose_name_plural = "Descuentos"

    def __str__(self):
        return f"{self.valor}% - {self.descripcion}"
