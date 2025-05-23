from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Hotel, Servicio, HotelServicios, Habitacion, RoomServicios
from reservations.models import Reserva
from django.db import transaction
from django.db.models import Q
from datetime import datetime

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

def registrar_hotel_view(request):
    if request.method == 'POST':
        try:
            hotel = registrar_hotel(
                nombre=request.POST['nombre'],
                direccion=request.POST['direccion'],
                ciudad=request.POST['ciudad'],
                pais=request.POST['pais'],
                telefono=request.POST['telefono'],
                email_contacto=request.POST['email_contacto'],
                categoria_estrellas=int(request.POST['categoria_estrellas']),
                descripcion_general=request.POST.get('descripcion_general', '')
            )
            messages.success(request, f'Hotel {hotel.nombre} registrado exitosamente.')
            return redirect('rooms:registrar_hotel')
        except Exception as e:
            messages.error(request, f'Error al registrar hotel: {str(e)}')
    return render(request, 'rooms/registrar_hotel.html')

def añadir_servicio(nombre_servicio, descripcion_servicio=''):
    with transaction.atomic():
        servicio = Servicio.objects.create(
            nombre_servicio=nombre_servicio,
            descripcion_servicio=descripcion_servicio
        )
        return servicio

def añadir_servicio_view(request):
    if request.method == 'POST':
        try:
            servicio = añadir_servicio(
                nombre_servicio=request.POST['nombre_servicio'],
                descripcion_servicio=request.POST.get('descripcion_servicio', '')
            )
            messages.success(request, f'Servicio {servicio.nombre_servicio} añadido exitosamente.')
            return redirect('rooms:añadir_servicio')
        except Exception as e:
            messages.error(request, f'Error al añadir servicio: {str(e)}')
    return render(request, 'rooms/añadir_servicio.html')

def asociar_servicio_hotel(hotel_id, servicio_id):
    with transaction.atomic():
        hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
        servicio = get_object_or_404(Servicio, servicio_id=servicio_id)
        hotel_servicio, created = HotelServicios.objects.get_or_create(hotel=hotel, servicio=servicio)
        return hotel_servicio

def asociar_servicio_hotel_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    if request.method == 'POST':
        try:
            servicio_id = request.POST['servicio_id']
            asociar_servicio_hotel(hotel_id, servicio_id)
            messages.success(request, 'Servicio asociado al hotel exitosamente.')
            return redirect('rooms:asociar_servicio_hotel', hotel_id=hotel_id)
        except Exception as e:
            messages.error(request, f'Error al asociar servicio: {str(e)}')
    servicios = Servicio.objects.all()
    return render(request, 'rooms/asociar_servicio_hotel.html', {'hotel': hotel, 'servicios': servicios})

def buscar_habitaciones_disponibles(hotel_id, fecha_inicio, fecha_fin, capacidad_minima, servicio_wifi=True):
    habitaciones = Habitacion.objects.filter(
        hotel_id=hotel_id,
        tipo_habitacion__capacidad_max__gte=capacidad_minima,
        estado='Disponible'
    )
    if servicio_wifi:
        wifi = Servicio.objects.get(nombre_servicio='WiFi Gratis')
        habitaciones = habitaciones.filter(
            habitacion_id__in=RoomServicios.objects.filter(servicio=wifi).values('habitacion_id')
        )
    reservas = Reserva.objects.filter(
        fecha_checkin__lte=fecha_fin,
        fecha_checkout__gte=fecha_inicio,
        estado_reserva__in=['Confirmada', 'Pendiente']
    ).values('habitacion_id')
    habitaciones_disponibles = habitaciones.exclude(habitacion_id__in=reservas)
    return habitaciones_disponibles

def buscar_habitaciones_disponibles_view(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    if request.method == 'POST':
        try:
            fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').date()
            capacidad_minima = int(request.POST['capacidad_minima'])
            servicio_wifi = request.POST.get('servicio_wifi', 'on') == 'on'
            habitaciones = buscar_habitaciones_disponibles(hotel_id, fecha_inicio, fecha_fin, capacidad_minima, servicio_wifi)
            return render(request, 'rooms/habitaciones_disponibles.html', {'hotel': hotel, 'habitaciones': habitaciones})
        except Exception as e:
            messages.error(request, f'Error al buscar habitaciones: {str(e)}')
    return render(request, 'rooms/buscar_habitaciones.html', {'hotel': hotel})

def listar_habitaciones_nunca_reservadas():
    habitaciones = Habitacion.objects.exclude(
        habitacion_id__in=Reserva.objects.values('habitacion_id')
    )
    return habitaciones

def listar_habitaciones_nunca_reservadas_view(request):
    habitaciones = listar_habitaciones_nunca_reservadas()
    return render(request, 'rooms/habitaciones_nunca_reservadas.html', {'habitaciones': habitaciones})