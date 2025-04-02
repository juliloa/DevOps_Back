from django.db import models

class Logs(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    affected_table = models.CharField(max_length=100)
    operation = models.CharField(max_length=20)
    previous_record = models.JSONField(blank=True, null=True)
    new_record = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'
