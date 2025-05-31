from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reseña
from .forms import ReseñaForm
from reservations.models import Reserva
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from datetime import datetime, timedelta
from rooms.models import Hotel

def calcular_puntuacion_media_hotel(hotel_id):
    puntuacion_media = Reseña.objects.filter(
        reserva__habitacion__hotel_id=hotel_id,
        visible=True
    ).aggregate(media=Avg('puntuacion'))['media'] or 0
    return puntuacion_media

def calcular_ingreso_hotel(hotel_id, dias=30):
    fecha_limite = datetime.now().date() - timedelta(days=dias)
    ingresos_facturados = Factura.objects.filter(
        reserva__habitacion__hotel_id=hotel_id,
        fecha_emision__gte=fecha_limite
    ).aggregate(total=Sum('monto_total'))['total'] or 0

    ingresos_pagados = Pago.objects.filter(
        factura__reserva__habitacion__hotel_id=hotel_id,
        fecha_pago__gte=fecha_limite
    ).aggregate(total=Sum('monto'))['total'] or 0

    return {
        'ingresos_facturados': ingresos_facturados,
        'ingresos_pagados': ingresos_pagados
    }

def calcular_puntuacion_media_hotel_view(request, hotel_id):
    puntuacion = calcular_puntuacion_media_hotel(hotel_id)
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    return render(request, 'reviews/puntuacion_hotel.html', {'hotel': hotel, 'puntuacion': puntuacion})

@login_required
def crear_reseña_view(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id, cliente__email=request.user.email)
    # Solo permitir si la reserva ya terminó y no existe reseña
    if reserva.fecha_checkout > timezone.now().date():
        messages.error(request, "Solo puedes dejar una reseña después de tu estadía.")
        return redirect('users:dashboard')
    if Reseña.objects.filter(reserva=reserva).exists():
        messages.warning(request, "Ya has dejado una reseña para esta reserva.")
        return redirect('users:dashboard')
    if request.method == 'POST':
        form = ReseñaForm(request.POST)
        if form.is_valid():
            reseña = form.save(commit=False)
            reseña.reserva = reserva
            reseña.save()
            messages.success(request, "¡Gracias por tu reseña!")
            return redirect('users:dashboard')
    else:
        form = ReseñaForm()
    return render(request, 'reviews/crear_reseña.html', {'form': form, 'reserva': reserva})