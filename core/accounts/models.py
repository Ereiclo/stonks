from django.db import models
from django.contrib.auth.models import User

"""
# Create your models here.
class Client(User):
    user = models.ForeignKey(User, related_name="users", null=True, on_delete=models.deletion.CASCADE)
    dni = models.CharField(max_length=7, unique=True)
"""

