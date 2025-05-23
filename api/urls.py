from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('hoteles/crear/', views.HotelCreateView.as_view(), name='hotel_create'),
    path('habitaciones/disponibles/', views.HabitacionesDisponiblesView.as_view(), name='habitaciones_disponibles'),
    path('promociones/crear/', views.PromocionCreateView.as_view(), name='promocion_create'),
    path('reservas/crear/', views.ReservaCreateView.as_view(), name='reserva_create'),
]