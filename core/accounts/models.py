from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager


class UserProfileManager(BaseUserManager):

    def create_user(self,dni,names,lastname,email,password):

        user = self.model(dni=dni,names=names,lastname=lastname,email=email)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,dni,names,lastname,email,password):
        user = self.create_user(dni,names,lastname,email,password)

        user.is_superuser = True
        user.save()

        return user

class Client(AbstractBaseUser,PermissionsMixin):
    dni = models.CharField(max_length=8,primary_key=True,unique=True)
    names = models.CharField(max_length=80)
    lastname = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['names','lastname','email']


    def get_id(self):
        return self.dni
    
    def __str__(self):
        return f"(Dni: {self.dni}, Names {self.names})"



