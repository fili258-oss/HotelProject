from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('hoteles/<int:hotel_id>/puntuacion/', views.calcular_puntuacion_media_hotel_view, name='calcular_puntuacion_media'),
]