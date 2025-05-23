from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

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
def logoutView(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:login')

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