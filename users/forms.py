from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
"""
class ApplicantCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name','email','password']

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                return forms.ValidationError('Las contraseñas no son iguales')
            return cd['password2']
    class Meta:
        model = User
        fields = ['phone_number', 'address', 'profile_picture', 'date_of_birth']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de teléfono'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dirección'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
"""