from django.db import models
import uuid

class Movements(models.Model):
    id = models.AutoField(primary_key=True)
    source_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='source_warehouse')
    destination_warehouse = models.ForeignKey('Warehouses', models.DO_NOTHING, db_column='destination_warehouse', related_name='movements_destination_warehouse_set')
    user = models.ForeignKey('Users', models.DO_NOTHING)
    variant = models.ForeignKey('ProductVariants', models.DO_NOTHING)
    quantity = models.IntegerField()
    date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)
    reason = models.TextField(blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        managed = False
        db_table = 'movements'