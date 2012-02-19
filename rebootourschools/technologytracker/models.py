from django.contrib.auth.models import User
from django.db import models





####
# District and School related field
####

class District(models.Model):
    full_name = models.CharField(max_length=60)
    district_code = models.CharField(max_length=10)
    state = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    county = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.district_code

class School(models.Model):
    district = models.ForeignKey(District)
    full_name = models.CharField(max_length=60)
    school_code = models.CharField(max_length=10)
        
    def __unicode__(self):
        return self.full_name 
        
    def computer_count(self):
        return u"%s" % ("num computers")
    computer_count.short_description = "Computers at this school"           


    
####
# User models
####

class TechTrackerAdminProfile(models.Model):
    """Super User for global reporting and account creation."""

    # Link to Django user model
    user = models.OneToOneField(User)

class DistrictUserProfile(models.Model):
    """District User for each district account."""

    # Link to Django user model
    user = models.OneToOneField(User)

    district = models.ForeignKey(District)

    def __unicode__(self):
        return u"%s/%s" % (self.user.username, self.district.full_name)



####
# Device models
####

class Computer(models.Model):
    school = models.ForeignKey(School)
    os = models.CharField(max_length=30)
    processor = models.CharField(max_length=30)
    hd_size = models.CharField(max_length=10)
    ram = models.CharField(max_length=30)
    monitor_size = models.CharField(max_length=30)
    
    class Meta:
        ordering = ('school',)
        
    def __unicode__(self):
        return u"%s %s %s %s" % (self.os, self.processor, self.ram, self.hd_size)

    
class LicensedSoftware(models.Model):
    school =  models.ForeignKey(School)
    product_name = models.CharField(max_length=30)
    software_type = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u"%s %s" % (self.product_name, self.publisher)


class Printer(models.Model):
    school =  models.ForeignKey(School)
    model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    kind = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u"%s %s" % (self.manufacturer, self.model)      


class Tablet(models.Model):
    school =  models.ForeignKey(School)
    model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    kind = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u"%s %s" % (self.manufacturer, self.model)

    
class MobileDevice(models.Model):
    school =  models.ForeignKey(School)
    model = models.CharField(max_length=30)
    manufacturer = models.CharField(max_length=30)
    kind = models.CharField(max_length=30)
    
    def __unicode__(self):
        return u"%s %s" % (self.manufacturer, self.model)
    
    
    
    
