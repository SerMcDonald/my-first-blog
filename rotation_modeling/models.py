from django.db import models
from django.utils import timezone

# Create your models here.
class RotationModel(models.Model):

    name = models.TextField(null=True)
    time_avel_data = models.TextField(null=True)
    ang_vel_data = models.TextField(null=True)
    time_thrust_data = models.TextField(null=True)
    comment = models.TextField(null=True)
    orbit_hight = models.IntegerField(null=True)
    cab_len = models.IntegerField(default=0)
    mas1 = models.IntegerField(default=0)
    mas2 = models.IntegerField(default=0)
    thrust = models.FloatField(default=0)
    published_date = models.DateTimeField(null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()