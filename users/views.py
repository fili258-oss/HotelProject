<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
=======
from django.shortcuts import render, redirect
from django.http import Http404
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
<<<<<<< HEAD
from .forms import LoginForm, ClienteCreationForm
from .models import Empleado, Rol, Cliente
from rooms.models import Hotel
from django.db import transaction

@login_required
def dashboardApplicant(request):
    return render(request, 'users/index.html')

def userLogin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
=======
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
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Inicio de sesión exitoso.')
                    return redirect('users:dashboard')
                else:
                    messages.error(request, 'El usuario no está activo.')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Formulario inválido.')
    else:
<<<<<<< HEAD
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

=======
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
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486
def register(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido.')
            return redirect('users:dashboard')
        else:
            messages.error(request, 'Error al crear la cuenta. Verifica los datos.')
    else:
        form = ClienteCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
<<<<<<< HEAD
def logoutView(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:login')
=======
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
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486

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

<<<<<<< HEAD
def registrar_empleado_view(request):
    if request.method == 'POST':
        try:
            empleado = registrar_empleado(
                hotel_id=int(request.POST['hotel_id']),
                rol_id=int(request.POST['rol_id']),
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                telefono=request.POST.get('telefono', ''),
                fecha_contratacion=datetime.strptime(request.POST['fecha_contratacion'], '%Y-%m-%d').date(),
                salario=float(request.POST['salario'])
            )
            messages.success(request, f'Empleado {empleado.nombre} registrado exitosamente.')
            return redirect('users:registrar_empleado')
        except Exception as e:
            messages.error(request, f'Error al registrar empleado: {str(e)}')
    hoteles = Hotel.objects.all()
    roles = Rol.objects.all()
    return render(request, 'users/registrar_empleado.html', {'hoteles': hoteles, 'roles': roles})
=======
def custom_404_view(request, exception):
    """
    Vista personalizada para manejar errores 404
    """
    return render(request, 'errors/404.html', status=404)
>>>>>>> 10cb3d09065e53b934e285ed69011f67feec2486
