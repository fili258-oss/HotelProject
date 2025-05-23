from django.db import models

class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email_contacto = models.EmailField()
    categoria_estrellas = models.PositiveSmallIntegerField()
    descripcion_general = models.TextField(blank=True)

    class Meta:
        db_table = 'hoteles'

    def __str__(self):
        return self.nombre

class TipoHabitacion(models.Model):
    tipo_habitacion_id = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    capacidad_max = models.PositiveIntegerField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'tipos_habitacion'

    def __str__(self):
        return self.nombre_tipo

class Servicio(models.Model):
    servicio_id = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=50)
    descripcion_servicio = models.TextField(blank=True)

    class Meta:
        db_table = 'servicios'

    def __str__(self):
        return self.nombre_servicio

class HotelServicios(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hotel_servicios'
        unique_together = ('hotel', 'servicio')

class Habitacion(models.Model):
    habitacion_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    numero_habitacion = models.CharField(max_length=10)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE)
    precio_por_noche = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='Disponible')

    class Meta:
        db_table = 'habitaciones'
        unique_together = ('hotel', 'numero_habitacion')

    def __str__(self):
        return f"{self.hotel.nombre} - Habitación {self.numero_habitacion}"

class RoomServicios(models.Model):
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    class Meta:
        db_table = 'room_servicios'
        unique_together = ('habitacion', 'servicio')