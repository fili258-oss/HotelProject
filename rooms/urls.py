from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('hoteles/crear/', views.registrar_hotel_view, name='registrar_hotel'),
    path('servicios/crear/', views.anadir_servicio_view, name='anadir_servicio'),
    path('hoteles/<int:hotel_id>/servicios/asociar/', views.asociar_servicio_hotel_view, name='asociar_servicio_hotel'),
    path('hoteles/<int:hotel_id>/habitaciones/disponibles/', views.buscar_habitaciones_disponibles_view, name='buscar_habitaciones_disponibles'),
    path('habitaciones/nunca-reservadas/', views.listar_habitaciones_nunca_reservadas_view, name='habitaciones_nunca_reservadas'),
    path('habitaciones/crear/', views.crear_habitacion_view, name='crear_habitacion'),
]