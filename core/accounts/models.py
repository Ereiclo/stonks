from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

dni_validator = RegexValidator(r'[0-9]{8}', 'DNI Inválido')
starting_money = 100000


class UserProfileManager(BaseUserManager):

    def create_user(self, dni, names, lastname, email, password):
        user = self.model(dni=dni, names=names, lastname=lastname, email=email, money=starting_money)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, dni, names, lastname, email, password):
        user = self.create_user(dni, names, lastname, email, password)

        user.is_superuser = True
        user.save()

        return user


class Client(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField(max_length=8, primary_key=True, unique=True, validators=[dni_validator])
    names = models.CharField(max_length=80)
    lastname = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    money = models.DecimalField(max_digits=12, decimal_places=2)

    objects = UserProfileManager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['names', 'lastname', 'email']

    def is_staff(self):
        return self.is_superuser

    def get_id(self):
        return self.dni

    def reset_money(self):
        self.money = starting_money

    def __str__(self):
        return f"(Dni: {self.dni}, Names {self.names})"
