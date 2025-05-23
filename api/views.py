#from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rooms.views import registrar_hotel, buscar_habitaciones_disponibles
from reservations.views import crear_promocion, crear_reserva
from datetime import datetime

class HotelCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            hotel = registrar_hotel(
                nombre=data['nombre'],
                direccion=data['direccion'],
                ciudad=data['ciudad'],
                pais=data['pais'],
                telefono=data['telefono'],
                email_contacto=data['email_contacto'],
                categoria_estrellas=data['categoria_estrellas'],
                descripcion_general=data.get('descripcion_general', '')
            )
            return Response({'hotel_id': hotel.hotel_id, 'nombre': hotel.nombre}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class HabitacionesDisponiblesView(APIView):
    def get(self, request):
        hotel_id = request.query_params.get('hotel_id')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        capacidad_minima = int(request.query_params.get('capacidad_minima', 1))
        servicio_wifi = request.query_params.get('servicio_wifi', 'true').lower() == 'true'
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            habitaciones = buscar_habitaciones_disponibles(hotel_id, fecha_inicio, fecha_fin, capacidad_minima, servicio_wifi)
            return Response([{'habitacion_id': h.habitacion_id, 'numero': h.numero_habitacion} for h in habitaciones], status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class PromocionCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            promocion = crear_promocion(
                codigo_promo=data['codigo_promo'],
                descripcion=data.get('descripcion', ''),
                descuento_porcentaje=float(data['descuento_porcentaje']) if data.get('descuento_porcentaje') else None,
                descuento_fijo=float(data['descuento_fijo']) if data.get('descuento_fijo') else None,
                fecha_inicio=datetime.strptime(data['fecha_inicio'], '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(data['fecha_fin'], '%Y-%m-%d').date(),
                activa=data.get('activa', True)
            )
            return Response({'promocion_id': promocion.promocion_id, 'codigo_promo': promocion.codigo_promo}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ReservaCreateView(APIView):
    def post(self, request):
        data = request.data
        try:
            reserva, factura = crear_reserva(
                cliente_id=data['cliente_id'],
                habitacion_id=data['habitacion_id'],
                fecha_checkin=datetime.strptime(data['fecha_checkin'], '%Y-%m-%d').date(),
                fecha_checkout=datetime.strptime(data['fecha_checkout'], '%Y-%m-%d').date(),
                numero_adultos=data['numero_adultos'],
                numero_ninos=data.get('numero_ninos', 0),
                codigo_promo=data.get('codigo_promo')
            )
            return Response({
                'reserva_id': reserva.reserva_id,
                'factura_id': factura.factura_id,
                'costo_total': float(factura.monto_total)
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)