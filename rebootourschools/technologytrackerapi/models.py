from django.db import models

# Create your models here.
class RunRecord(models.Model):
    runtime = models.DateTimeField()
