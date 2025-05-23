from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Promocion, Reserva, ReservaPromociones, Factura, ItemFactura, Pago
from rooms.models import Hotel, Habitacion
from users.models import Cliente
from django.db import transaction
from django.db.models import Sum, Count
from datetime import datetime, timedelta, date

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

def crear_promocion_view(request):
    if request.method == 'POST':
        try:
            promocion = crear_promocion(
                codigo_promo=request.POST['codigo_promo'],
                descripcion=request.POST.get('descripcion', ''),
                descuento_porcentaje=float(request.POST['descuento_porcentaje']) if request.POST.get('descuento_porcentaje') else None,
                descuento_fijo=float(request.POST['descuento_fijo']) if request.POST.get('descuento_fijo') else None,
                fecha_inicio=datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%d').date(),
                activa=request.POST.get('activa', 'on') == 'on'
            )
            messages.success(request, f'Promoción {promocion.codigo_promo} creada exitosamente.')
            return redirect('reservations:crear_promocion')
        except Exception as e:
            messages.error(request, f'Error al crear promoción: {str(e)}')
    return render(request, 'reservations/crear_promocion.html')

def crear_reserva(cliente_id, habitacion_id, fecha_checkin, fecha_checkout, numero_adultos, numero_ninos=0, codigo_promo=None):
    with transaction.atomic():
        habitacion = get_object_or_404(Habitacion, habitacion_id=habitacion_id, estado='Disponible')
        cliente = get_object_or_404(Cliente, cliente_id=cliente_id)
        
        reservas = Reserva.objects.filter(
            habitacion_id=habitacion_id,
            fecha_checkin__lte=fecha_checkout,
            fecha_checkout__gte=fecha_checkin,
            estado_reserva__in=['Confirmada', 'Pendiente']
        )
        if reservas.exists():
            raise ValueError("Habitación no disponible en el rango de fechas")
        
        if fecha_checkin >= fecha_checkout:
            raise ValueError("La fecha de check-in debe ser anterior a la de check-out")

        dias = (fecha_checkout - fecha_checkin).days
        costo_base = habitacion.precio_por_noche * dias

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
        if costo_total < 0:
            raise ValueError("El costo total no puede ser negativo")

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

        if promocion:
            ReservaPromociones.objects.create(reserva=reserva, promocion=promocion)

        iva_rate = 0.16
        monto_iva = costo_total * iva_rate
        factura = Factura.objects.create(
            reserva=reserva,
            monto_total=costo_total + monto_iva,
            iva=iva_rate,
            estado_pago='Pendiente'
        )

        ItemFactura.objects.create(
            factura=factura,
            concepto=f"Estancia {dias} noches",
            cantidad=1,
            precio_unitario=costo_total,
            subtotal=costo_total
        )

        return reserva, factura

def crear_reserva_view(request):
    if request.method == 'POST':
        try:
            reserva, factura = crear_reserva(
                cliente_id=int(request.POST['cliente_id']),
                habitacion_id=int(request.POST['habitacion_id']),
                fecha_checkin=datetime.strptime(request.POST['fecha_checkin'], '%Y-%m-%d').date(),
                fecha_checkout=datetime.strptime(request.POST['fecha_checkout'], '%Y-%m-%d').date(),
                numero_adultos=int(request.POST['numero_adultos']),
                numero_ninos=int(request.POST.get('numero_ninos', 0)),
                codigo_promo=request.POST.get('codigo_promo')
            )
            messages.success(request, f'Reserva {reserva.reserva_id} creada exitosamente.')
            return redirect('reservations:crear_reserva')
        except Exception as e:
            messages.error(request, f'Error al crear reserva: {str(e)}')
    clientes = Cliente.objects.all()
    habitaciones = Habitacion.objects.all()
    promociones = Promocion.objects.filter(activa=True)
    return render(request, 'reservations/crear_reserva.html', {'clientes': clientes, 'habitaciones': habitaciones, 'promociones': promociones})

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

def calcular_ingreso_hotel_view(request, hotel_id):
    ingresos = calcular_ingreso_hotel(hotel_id)
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    return render(request, 'reservations/ingresos_hotel.html', {'hotel': hotel, 'ingresos': ingresos})

def listar_promociones_activas():
    promociones = Promocion.objects.filter(
        activa=True,
        fecha_inicio__lte=date.today(),
        fecha_fin__gte=date.today()
    ).annotate(uso=Count('reservapromociones'))
    return promociones

def listar_promociones_activas_view(request):
    promociones = listar_promociones_activas()
    return render(request, 'reservations/promociones_activas.html', {'promociones': promociones})

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

def vista_ocupacion_actual_view(request, hotel_id):
    ocupacion = vista_ocupacion_actual(hotel_id)
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    return render(request, 'reservations/ocupacion_hotel.html', {'hotel': hotel, 'ocupacion': ocupacion})