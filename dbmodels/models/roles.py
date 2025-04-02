from django.db import models

class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'roles'