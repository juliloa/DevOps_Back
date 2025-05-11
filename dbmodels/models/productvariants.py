from django.db import models

class ProductVariants(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', on_delete=models.DO_NOTHING, related_name='variants')
    variant_code = models.CharField(max_length=100, unique=True)  
    attributes = models.JSONField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False  
        db_table = 'product_variants'

    def __str__(self):
        return self.variant_code