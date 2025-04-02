from django.db import models

class Inventory(models.Model):
    id = models.AutoField(primary_key=True) 
    variant = models.ForeignKey('ProductVariants', models.DO_NOTHING)
    warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING)
    quantity = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'inventory'
        unique_together = (('variant', 'warehouse'),)
