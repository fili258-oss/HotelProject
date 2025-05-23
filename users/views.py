from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
#from .forms import UserProfileForm
#from .models import UserProfile
from .models import User

@login_required
def dashboardApplicant(request):
    return render(request, 'dashboard/index.html')

def userLogin(request):    
    if request.method == 'POST': 
                              
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            #print("user", user)
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
@login_required	
def logoutView(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('users:login')
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