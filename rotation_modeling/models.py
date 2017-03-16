from django.db import models

# Create your models here.
class RotationModel(models.Model):

    time_avel_data = models.TextField()
    ang_vel_data = models.TextField()
    comment = models.TextField()
    orbit_hight = models.IntegerField()
    cab_len = models.IntegerField()
    mas1 = models.IntegerField()
    mas2 = models.IntegerField()
    thrust = models.FloatField()