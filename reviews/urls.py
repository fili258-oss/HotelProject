from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('hoteles/<int:hotel_id>/puntuacion/', views.calcular_puntuacion_media_hotel_view, name='calcular_puntuacion_media'),
    path('reserva/<int:reserva_id>/crear/', views.crear_reseña_view, name='crear_reseña'),
]