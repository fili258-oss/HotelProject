from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # Perfil de usuario
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # Cambio de contraseña
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change_form.html',
        success_url='/accounts/profile/'
    ), name='password_change'),
]