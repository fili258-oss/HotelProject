#from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Promocion, Reserva, Factura, ItemFactura
from django.db import transaction
from datetime import datetime

def crear_promocion(codigo_promo, descripcion, descuento_porcentaje=None, descuento_fijo=None, fecha_inicio=None, fecha_fin=None, activa=True):
    with transaction.atomic():
        promocion = Promocion.objects.create(
            codigo_promo=codigo_promo,
            descripcion=descripcion,
            descuento_porcentaje=descuento_porcentaje,
            descuento_fijo=descuento_fijo,
            fecha_inicio=fecha_inicio or datetime.now().date(),
            fecha_fin=fecha_fin,
            activa=activa
        )
        return promocion
    
from django.db.models import Count
from datetime import date

def listar_promociones_activas():
    promociones = Promocion.objects.filter(
        activa=True,
        fecha_inicio__lte=date.today(),
        fecha_fin__gte=date.today()
    ).annotate(uso=Count('reservapromociones'))
    return promociones

def vista_ocupacion_actual(hotel_id):
    fecha_actual = date.today()
    total_habitaciones = Habitacion.objects.filter(hotel_id=hotel_id).count()
    ocupadas = Reserva.objects.filter(
        habitacion__hotel_id=hotel_id,
        fecha_checkin__lte=fecha_actual,
        fecha_checkout__gte=fecha_actual,
        estado_reserva='Confirmada'
    ).count()
    return {
        'hotel_id': hotel_id,
        'total_habitaciones': total_habitaciones,
        'ocupadas': ocupadas,
        'disponibles': total_habitaciones - ocupadas,
        'porcentaje_ocupacion': (ocupadas / total_habitaciones * 100) if total_habitaciones else 0
    }

def crear_reserva(cliente_id, habitacion_id, fecha_checkin, fecha_checkout, numero_adultos, numero_ninos=0, codigo_promo=None):
    with transaction.atomic():
        # Validar disponibilidad
        habitacion = get_object_or_404(Habitacion, habitacion_id=habitacion_id, estado='Disponible')
        cliente = get_object_or_404('users.Cliente', cliente_id=cliente_id)
        
        reservas = Reserva.objects.filter(
            habitacion_id=habitacion_id,
            fecha_checkin__lte=fecha_checkout,
            fecha_checkout__gte=fecha_checkin,
            estado_reserva__in=['Confirmada', 'Pendiente']
        )
        if reservas.exists():
            raise ValueError("Habitación no disponible en el rango de fechas")

        # Calcular días de estancia
        dias = (fecha_checkout - fecha_checkin).days
        costo_base = habitacion.precio_por_noche * dias

        # Aplicar promoción si es válida
        descuento = 0
        promocion = None
        if codigo_promo:
            promocion = get_object_or_404(
                Promocion,
                codigo_promo=codigo_promo,
                activa=True,
                fecha_inicio__lte=date.today(),
                fecha_fin__gte=date.today()
            )
            if promocion.descuento_porcentaje:
                descuento = costo_base * (promocion.descuento_porcentaje / 100)
            elif promocion.descuento_fijo:
                descuento = promocion.descuento_fijo

        costo_total = costo_base - descuento

        # Crear reserva
        reserva = Reserva.objects.create(
            cliente_id=cliente_id,
            habitacion=habitacion,
            fecha_checkin=fecha_checkin,
            fecha_checkout=fecha_checkout,
            numero_adultos=numero_adultos,
            numero_ninos=numero_ninos,
            costo_total_estimado=costo_total,
            estado_reserva='Pendiente'
        )

        # Asociar promoción
        if promocion:
            ReservaPromociones.objects.create(reserva=reserva, promocion=promocion)

        # Crear factura inicial
        iva_rate = 0.16  # Ejemplo: 16% IVA
        monto_iva = costo_total * iva_rate
        factura = Factura.objects.create(
            reserva=reserva,
            monto_total=costo_total + monto_iva,
            iva=iva_rate,
            estado_pago='Pendiente'
        )

        # Crear item de factura
        ItemFactura.objects.create(
            factura=factura,
            concepto=f"Estancia {dias} noches",
            cantidad=1,
            precio_unitario=costo_total,
            subtotal=costo_total
        )

        return reserva, factura