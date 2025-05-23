from django.shortcuts import render

# Create your views here.
from django.db.models import Avg
from .models import Reseña
from reservations.models import Reserva
from rooms.models import Hotel

def calcular_puntuacion_media_hotel(hotel_id):
    puntuacion_media = Reseña.objects.filter(
        reserva__habitacion__hotel_id=hotel_id,
        visible=True
    ).aggregate(media=Avg('puntuacion'))['media'] or 0
    return puntuacion_media

from django.db.models import Sum
from datetime import datetime, timedelta

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