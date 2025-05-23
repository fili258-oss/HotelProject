from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('', views.userLogin, name='login'),
    path('logout/', views.logoutView, name='logout'), 
    
    # Perfil de usuario
    #path('profile/', views.profile, name='profile'),
    #path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard', views.dashboardApplicant, name='dashboard'),
    # Cambio de contraseña
        
]