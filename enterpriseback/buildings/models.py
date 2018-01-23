from __future__ import unicode_literals

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import Transpose

# Create your models here.


class Building(models.Model):
    adress = models.CharField(max_length=300)
    location_description = models.TextField(blank=True)
    building_apartments = models.IntegerField(blank=True, null=True)
    #picture = models.ImageField(upload_to='building/', blank=True, null=True)
    picture = ProcessedImageField(upload_to='building/',processors=[Transpose()], format='JPEG', blank=True, null=True)

    def __unicode__(self):
        return self.adress

    class Meta:
        ordering = ('adress',)


class Department(models.Model):
    building = models.ForeignKey(Building,on_delete=models.CASCADE)
    number_of_apartment = models.CharField(max_length=50, verbose_name='Apartment Number',default="", blank=True)
    type_department = models.CharField(max_length=50, verbose_name='Type')
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    rent = models.FloatField(
            blank=True, null=True,
            help_text="Amount of money per month")
    deposit = models.FloatField(
            blank=True, null=True,
            help_text="Amount of money $$$ for deposit")
    parking = models.CharField(max_length=100,blank=True)
    pets = models.CharField(max_length=50,blank=True)
    #preguntar si no quieren un campo de multiplechoice
    utilities = models.CharField(max_length=200,blank=True)
    #preguntar si no quieren un campo de multiplechoice
    kitchen = models.CharField(max_length=200,blank=True)
    #OPcion de 1 o no, 
    laundry = models.CharField(max_length=100,blank=True)
    #preguntar tipos de licencias
    #OPT_LEASE=(
    #    ('townhome','Town Home'),
    #    ('studenthome','Student Home'),
    #    )
    lease_term = models.CharField(max_length=50,blank=True)
    #Unit Description
    unit_description = models.TextField()

    def __unicode__(self):
        return "%s"%(self.building)

    class Meta:
        ordering = ('building',) 


class NearbyAtraction(models.Model):
    titulo_img = models.CharField(max_length=100, verbose_name='Name of Amenitie', help_text='Location Description')
    #picture = models.ImageField(upload_to='building/NearbyAtraction/')
    picture = ProcessedImageField(upload_to='building/NearbyAtraction/',processors=[Transpose()], format='JPEG')
    building = models.ForeignKey(Building,on_delete=models.CASCADE, blank=True, null=True)
    def __unicode__(self):
        if self.titulo_img:
            return self.titulo_img
        else:
            return "%s"%self.id

class DepartmenGalery(models.Model):
    titulo_img = models.CharField(max_length=100, verbose_name='Name of Amenitie', help_text='Location Description', blank=True)
    #picture = models.ImageField(upload_to='building/Departments/')
    picture = ProcessedImageField(upload_to='building/Departments/',processors=[Transpose()], format='JPEG')
    departmen = models.ForeignKey(Department,on_delete=models.CASCADE, blank=True, null=True)
    def __unicode__(self):
        if self.titulo_img:
            return self.titulo_img
        else:
            return "%s"%self.id