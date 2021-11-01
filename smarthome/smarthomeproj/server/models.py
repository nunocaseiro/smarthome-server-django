from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Create your models here.
class Home(models.Model):
    name = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)
    key = models.CharField(
           max_length = 10,
           editable= True,
           null = True,
           unique=True)

    def __str__(self):
        return "%s" % (self.name) 

class Room(models.Model):
    name = models.CharField(max_length=20)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20)
    testing = models.BooleanField(default=True)
    ROOM_TYPE = [
        ("bedroom", 'BEDROOM'),
        ("garage", 'GARAGE'),
        ("kitchen", 'KITCHEN'),
        ("living", 'LIVING ROOM'),
        ("bathroom", 'BATHROOM'),
        ("other", 'OTHER')
    ]
    roomtype = models.CharField(max_length=20,choices=ROOM_TYPE, default="bedroom")
    
    def __str__(self):
        return "%s" % (self.name)

class Sensor(models.Model):
    SENSOR_TYPE = [
        ("led", 'LED'),
        ("plug", 'PLUG'),
        ("camera", 'CAMERA'),
        ("servo", 'SERVO'),
        ("motion",'MOTION'),
        ("temperature","TEMPERATURE"),
        ("luminosity", "LUMINOSITY")
    ]
    name = models.CharField(max_length=20)
    sensortype = models.CharField(max_length=20,choices=SENSOR_TYPE, default="Undefined")
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    ios = models.BooleanField(default=True)
    actuator = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    gpio = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(40),
            MinValueValidator(1)
        ])
    temp_lim = models.DecimalField(max_digits=3, decimal_places=1, null = True, blank = True)
    lux_lim = models.IntegerField(null = True, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    auto = models.BooleanField(default=True)
    
    def __str__(self):
        return "%s" % (self.name)

class SensorValue(models.Model):
    idsensor  = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Id sensor: %s ||| Value: ||| %f Created: %s" % (self.idsensor, self.value, self.created_at)

class Vehicle(models.Model):
    brand = models.CharField(max_length=20)
    licenseplate = models.CharField(max_length=6)
    model = models.CharField(max_length=20)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, default= 1)
    year = models.IntegerField(validators=[
            MaxValueValidator(2050),
            MinValueValidator(1900)
        ])
    def __str__(self):
        return "%s %s" % (self.licenseplate, self.brand)

class Photo(models.Model):
    photo = models.ImageField(upload_to='static/photos')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.photo)

class Favourite(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('sensor', 'user',)
    def __str__(self):
        return "%s %s" % (self.sensor.name, self.user.username)
        
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home = models.ForeignKey(Home, on_delete=models.CASCADE, null = True)
    photo = models.ImageField(upload_to='static/profile', null = True, blank= True)
    
class Notification(models.Model):
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    notification = models.CharField(max_length=50)
    licensePlate = models.CharField(max_length = 6, null = True)
    description = models.CharField(max_length = 20, null = True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

def create_new_ref_number():
      return str(random.randint(1000000000, 9999999999))

class HouseKey(models.Model):
      key = models.CharField(
           max_length = 10,
           blank=True,
           editable=False,
           unique=True,
           default=create_new_ref_number()
      )
      def __str__(self):
        return "%s" % (self.key)




