from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
<<<<<<< HEAD
    path('', views.userLogin, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('dashboard/', views.dashboardApplicant, name='dashboard'),
    path('register/', views.register, name='register'),
    path('empleados/registrar/', views.registrar_empleado_view, name='registrar_empleado'),
=======
    # Autenticación
    # Página principal con validación
    path('', views.home, name='home'),
    path('login', views.userLogin, name='login'),
    path('logout', views.logoutView, name='logout'), 
    path('dashboard', views.dashboardApplicant, name='dashboard')
    # Cambio de contraseña
        
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486
]