from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from .models import Empleado, Rol
from rooms.models import Hotel
from django.db import transaction
#from .forms import UserProfileForm
#from .models import UserProfile
from .models import User

def home(request):
    """
    Vista principal que valida si el usuario está autenticado
    """
    if request.user.is_authenticated:
        # Si está autenticado, redirige al dashboard
        return redirect('users:dashboard')
    else:
        # Si no está autenticado, redirige al login
        return redirect('users:login')

def userLogin(request):    
    if request.method == 'POST': 
                              
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                
                if user.is_active:
                    login(request, user)
                    return redirect('users:dashboard')
                else:
                    return render(request, 'auth/login.html', {
                        'error': 'El usuario no esta activo'})
            else:
                return render(request, 'auth/login.html', {
                        'error': 'Usuario o contraseña incorrectosss'})        
    else:
        return render(request, 'auth/login.html')
    
@login_required
def dashboardApplicant(request):
    """
    Vista del dashboard (requiere autenticación)
    """
    return render(request, 'dashboard/index.html')

def logoutView(request):
    """
    Vista para cerrar sesión
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:home')
"""""
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido a Hotel Paraíso.')
            return redirect('core:home')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})
"""""
"""""
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    return render(request, 'users/profile.html', {'profile': profile})
"""""

"""""
@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/edit_profile.html', {'form': form})

"""""

def registrar_empleado(hotel_id, rol_id, nombre, apellido, email, telefono, fecha_contratacion, salario):
    with transaction.atomic():
        hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
        rol = get_object_or_404(Rol, rol_id=rol_id)
        empleado = Empleado.objects.create(
            hotel=hotel,
            rol=rol,
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            fecha_contratacion=fecha_contratacion,
            salario=salario
        )
        return empleado

def custom_404_view(request, exception):
    """
    Vista personalizada para manejar errores 404
    """
    return render(request, 'errors/404.html', status=404)
