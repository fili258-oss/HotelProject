from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    """
    Modelo de usuario que usa solo los campos por defecto de Django:
    - username
    - first_name
    - last_name
    - email
    - password
    - groups
    - user_permissions
    - is_staff
    - is_active
    - is_superuser
    - last_login
    - date_joined
    """
    
    def __str__(self):
        return self.user.username
        