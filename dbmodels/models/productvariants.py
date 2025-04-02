from django.db import models

class ProductVariants(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    attribute_name = models.CharField(max_length=255)
    attribute_value = models.CharField(max_length=255)
    stock = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_variants'
