from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticación
    # Página principal con validación
    path('', views.home, name='home'),
    path('login', views.userLogin, name='login'),
    path('logout', views.logoutView, name='logout'), 
    path('dashboard', views.dashboardApplicant, name='dashboard')
    # Cambio de contraseña
        
]