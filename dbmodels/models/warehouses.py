from django.db import models

class Warehouses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    location = models.TextField()
    max_capacity = models.IntegerField(null=False)
    open_hours = models.CharField(max_length=50, default='06:00-22:00')
    coordinates = models.JSONField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'warehouses'
