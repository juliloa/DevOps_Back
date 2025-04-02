from django.db import models
from .roles import Roles

class Users(models.Model):
    id_card = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, blank=True, null=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    status = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'