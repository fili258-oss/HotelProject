from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('promociones/crear/', views.crear_promocion_view, name='crear_promocion'),
    path('reservas/crear/', views.crear_reserva_view, name='crear_reserva'),
    path('hoteles/<int:hotel_id>/ingresos/', views.calcular_ingreso_hotel_view, name='calcular_ingreso_hotel'),
    path('promociones/activas/', views.listar_promociones_activas_view, name='listar_promociones_activas'),
    path('hoteles/<int:hotel_id>/ocupacion/', views.vista_ocupacion_actual_view, name='vista_ocupacion_actual'),
]