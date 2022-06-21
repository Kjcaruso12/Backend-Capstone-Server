from django.db import models
from django.contrib.auth.models import User

class InventoryUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    admin = models.BooleanField(default=False)
