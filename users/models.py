from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """
    Modelo de usuario que usa solo los campos por defecto de Django:
    - username
    - first_name
    - last_name
    - email
    - password
    - groups
    - user_permissions
    - is_staff
    - is_active
    - is_superuser
    - last_login
    - date_joined
    """
    
    def __str__(self):
        return self.user.username
        
        
from django.db import models
from django.utils import timezone

class Rol(models.Model):
    rol_id = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion_rol = models.TextField(blank=True)

    class Meta:
        db_table = 'roles'

    def __str__(self):
        return self.nombre_rol

class Cliente(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(default=timezone.now)
    preferencias = models.TextField(blank=True)

    class Meta:
        db_table = 'clientes'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(models.Model):
    empleado_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey('rooms.Hotel', on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'empleados'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"