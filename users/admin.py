#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cliente, Rol, Empleado

admin.site.register(Cliente)
admin.site.register(Rol)
admin.site.register(Empleado)
