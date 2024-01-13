from django.db import models
from home.models import Salons
from django.contrib.auth.models import User
# from django.conf import settings
# from home.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone


class Services(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SalonAndServices(models.Model):
    salon = models.ForeignKey(Salons, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    time = models.CharField(max_length=5)
    price = models.FloatField()

    def __str__(self):
        return self.service.name

@receiver(pre_save, sender=SalonAndServices)
def check_before_save(sender, instance, **kwargs):
    print('inside check before save')
    obj = SalonAndServices.objects.filter(salon=instance.salon, service=instance.service).first()
    print(f'obj:{obj}')
    if obj is not None:
        raise ValidationError('A duplicate entry is already exist.')


class Slots(models.Model):
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    salon = models.ForeignKey(Salons, on_delete=models.DO_NOTHING)
    services = models.TextField()
    price = models.FloatField()
    time = models.CharField(max_length=5)
    created_on = models.DateTimeField(default=timezone.now)
    canceled_on = models.DateTimeField(default=timezone.now)
    canceled_by = models.CharField(max_length=10, choices=[('customer','Customer'), ('salon', 'Salon')])
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.customer.username

class UserLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
