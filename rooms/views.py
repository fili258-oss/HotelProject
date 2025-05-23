from django.shortcuts import get_object_or_404
from .models import Hotel, Servicio, HotelServicios
from django.db import transaction

def registrar_hotel(nombre, direccion, ciudad, pais, telefono, email_contacto, categoria_estrellas, descripcion_general=''):
    with transaction.atomic():
        hotel = Hotel.objects.create(
            nombre=nombre,
            direccion=direccion,
            ciudad=ciudad,
            pais=pais,
            telefono=telefono,
            email_contacto=email_contacto,
            categoria_estrellas=categoria_estrellas,
            descripcion_general=descripcion_general
        )
        return hotel
    
def añadir_servicio(nombre_servicio, descripcion_servicio=''):
    with transaction.atomic():
        servicio = Servicio.objects.create(
            nombre_servicio=nombre_servicio,
            descripcion_servicio=descripcion_servicio
        )
        return servicio
    
def asociar_servicio_hotel(hotel_id, servicio_id):
    with transaction.atomic():
        hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
        servicio = get_object_or_404(Servicio, servicio_id=servicio_id)
        hotel_servicio, created = HotelServicios.objects.get_or_create(hotel=hotel, servicio=servicio)
        return hotel_servicio
    
def listar_habitaciones_nunca_reservadas():
    habitaciones = Habitacion.objects.exclude(
        habitacion_id__in=Reserva.objects.values('habitacion_id')
    )
    return habitaciones

