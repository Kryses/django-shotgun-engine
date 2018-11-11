from django.db import models

class Asset(models.Model):
    code = models.CharField()