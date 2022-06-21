from django.db import models

class Group(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    label = models.CharField(max_length=100)