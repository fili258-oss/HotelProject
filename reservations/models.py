from django.db import models
from django.utils import timezone

class Promocion(models.Model):
    promocion_id = models.AutoField(primary_key=True)
    codigo_promo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    descuento_fijo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'promociones'

    def __str__(self):
        return self.codigo_promo

class Reserva(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey('users.Cliente', on_delete=models.CASCADE)
    habitacion = models.ForeignKey('rooms.Habitacion', on_delete=models.CASCADE)
    empleado_checkin = models.ForeignKey('users.Empleado', on_delete=models.SET_NULL, null=True, blank=True, related_name='checkin_reservas')
    empleado_checkout = models.ForeignKey('users.Empleado', on_delete=models.SET_NULL, null=True, blank=True, related_name='checkout_reservas')
    fecha_reserva = models.DateTimeField(default=timezone.now)
    fecha_checkin = models.DateField()
    fecha_checkout = models.DateField()
    numero_adultos = models.PositiveIntegerField()
    numero_ninos = models.PositiveIntegerField(default=0)
    estado_reserva = models.CharField(max_length=20, default='Pendiente')
    costo_total_estimado = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'reservas'

    def __str__(self):
        return f"Reserva {self.reserva_id} - {self.cliente}"

class ReservaPromociones(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    promocion = models.ForeignKey(Promocion, on_delete=models.CASCADE)

    class Meta:
        db_table = 'reserva_promociones'
        unique_together = ('reserva', 'promocion')

class Factura(models.Model):
    factura_id = models.AutoField(primary_key=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    empleado_emisor = models.ForeignKey('users.Empleado', on_delete=models.SET_NULL, null=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2)
    estado_pago = models.CharField(max_length=20, default='Pendiente')

    class Meta:
        db_table = 'facturas'

    def __str__(self):
        return f"Factura {self.factura_id} - Reserva {self.reserva.reserva_id}"

class ItemFactura(models.Model):
    item_factura_id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'items_factura'

    def __str__(self):
        return f"Item {self.concepto} - Factura {self.factura.factura_id}"

class Pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    referencia_pago = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'pagos'

    def __str__(self):
        return f"Pago {self.pago_id} - Factura {self.factura.factura_id}"