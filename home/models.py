from django.db import models
# from django.contrib.gis.db import models as gismodels
from django.contrib.auth.models import AbstractUser, Permission

STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jammu and Kashmir', 'Jammu and Kashmir'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Chandigarh', 'Chandigarh'),
        ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('Delhi', 'Delhi'),
        ('Lakshadweep', 'Lakshadweep'),
        ('Puducherry', 'Puducherry'),
    ]

COUNTRY_CHOICES = [
        ('Afghanistan', 'Afghanistan'),
        ('Argentina', 'Argentina'),
        ('Australia', 'Australia'),
        ('Brazil', 'Brazil'),
        ('Canada', 'Canada'),
        ('China', 'China'),
        ('Egypt', 'Egypt'),
        ('France', 'France'),
        ('Germany', 'Germany'),
        ('Greece', 'Greece'),
        ('India', 'India'),
        ('Indonesia', 'Indonesia'),
        ('Iran', 'Iran'),
        ('Italy', 'Italy'),
        ('Japan', 'Japan'),
        ('Mexico', 'Mexico'),
        ('Netherlands', 'Netherlands'),
        ('New Zealand', 'New Zealand'),
        ('Nigeria', 'Nigeria'),
        ('Pakistan', 'Pakistan'),
        ('Peru', 'Peru'),
        ('Russia', 'Russia'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('South Africa', 'South Africa'),
        ('South Korea', 'South Korea'),
        ('Spain', 'Spain'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Thailand', 'Thailand'),
        ('Turkey', 'Turkey'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Emirates', 'United Arab Emirates'),
        ('United Kingdom', 'United Kingdom'),
        ('United States', 'United States'),
        ('Vietnam', 'Vietnam'),
    ]


# class CustomUser(AbstractUser):
#     user_type = models.CharField(max_length=10, choices=[('customer','Customer'),('shopkeeper','Shopkeeper')])

class City(models.Model):
    name = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


class Salons(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='salon_images/')
    image_url = models.TextField(null=True, blank=True)
    mobile = models.IntegerField()
    # coordinate = gismodels.PointField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_link = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    pincode = models.TextField()
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    state = models.CharField(max_length=50, choices=STATE_CHOICES)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)

    def __str__(self):
        return self.name
