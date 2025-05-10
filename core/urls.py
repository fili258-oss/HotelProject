from django.urls import path
from . import views

# Define un namespace para esta aplicación
app_name = 'core'

urlpatterns = [
    # Ruta para la página de inicio
    # La ruta vacía '' corresponde a la página principal
    path('', views.home, name='home'),
    
    # Puedes agregar más rutas a medida que desarrolles más vistas
    # Por ejemplo:
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
]