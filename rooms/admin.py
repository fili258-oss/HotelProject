#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Hotel, TipoHabitacion, Servicio, HotelServicios, Habitacion, RoomServicios

admin.site.register(Hotel)
admin.site.register(TipoHabitacion)
admin.site.register(Servicio)
admin.site.register(HotelServicios)
admin.site.register(Habitacion)
admin.site.register(RoomServicios)