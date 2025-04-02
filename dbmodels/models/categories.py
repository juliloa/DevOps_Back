from django.db import models


class Categories(models.Model):
    id = models.AutoField(primary_key=True) 
    name = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'categories'
