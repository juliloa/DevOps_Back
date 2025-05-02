from django.db import models
import uuid

class Movements(models.Model):
    id = models.AutoField(primary_key=True)
    source_warehouse = models.ForeignKey('Warehouses', models.CASCADE, db_column='source_warehouse')
    destination_warehouse = models.ForeignKey('Warehouses', models.CASCADE, db_column='destination_warehouse', related_name='movements_destination_warehouse_set')
    user = models.ForeignKey('Users', models.CASCADE,db_column='user_id',to_field='id_card')
    variant = models.ForeignKey('ProductVariants', models.CASCADE,  db_column='variant_id')
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    reason = models.TextField(blank=True, null=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    class Meta:
        managed = False
        db_table = 'movements'

    def __str__(self):
        return f'Movimiento {self.id} - {self.variant} ({self.status})'

