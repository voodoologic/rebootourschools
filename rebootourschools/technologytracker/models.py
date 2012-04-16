from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

####
# Choices
####    

OS_CHOICES = (
    ('OSX', 'OS X'),
    ('LINUX', 'Linux'),
    ('WINDOWS', 'Windows'),
)

HD_SIZE_CHOICES = (
    ('60', '60 GB'),
    ('128', '128 GB'),
    ('250', '250 GB'),
)

RAM_SIZE_CHOICES = (
    ('1', '1 GB'),
    ('2', '2 GB'),
    ('4', '4 GB'),
    ('8', '8 GB'),
)

MONITOR_SIZE_CHOICES = (
    ('12', '12"'),
    ('13', '13"'),
    ('14', '14"'),
    ('15', '15"'),
    ('16', '16"'),
    ('17', '17"'),
    ('18', '18"'),
    ('19', '19"'),
    ('20', '20"'),
    ('21', '21"'),
    ('22', '22"'),
    ('23', '23"'),
    ('24', '24"'),
)



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

    SCHOOL_TYPE_CHOICES = (
        (1, 'Elementary School'),
        (2, 'Junior High School'),
        (3, 'High School'),
    )

    district = models.ForeignKey(District)
    full_name = models.CharField(max_length=60)
    school_code = models.CharField(max_length=10, null=True)
    school_type = models.SmallIntegerField(choices=SCHOOL_TYPE_CHOICES)
    student_count = models.PositiveIntegerField(null=True)
    teacher_count = models.PositiveIntegerField(null=True)

    def __unicode__(self):
        return self.full_name 
        
    def computer_count(self):
        return u"%s" % ("num computers")	
    computer_count.short_description = "Computers at this school"           

    class Meta:
        ordering = ['school_type']


class SchoolRoom(models.Model):

    SCHOOL_ROOM_TYPE_CHOICES = (
        (1, 'Class Room'),
        (2, 'Lab'),
    )

    CONNECTION_TYPE_CHOICES = (
        (1, 'Wired'),
        (2, 'Wireless'),
        (3, 'Mixed'),
    )

    room_name = models.CharField(max_length=60)
    room_description = models.TextField()
    room_connection_speed = models.IntegerField(null=True)
    room_connection_count = models.SmallIntegerField(null=True)
    room_connection_type = models.SmallIntegerField(choices=CONNECTION_TYPE_CHOICES,null=True)
    school_room_type = models.SmallIntegerField(choices=SCHOOL_ROOM_TYPE_CHOICES)



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


class DistrictAsset(models.Model):
    district = models.ForeignKey(District)
    school = models.ForeignKey(School, null=True)
    room = models.ForeignKey(SchoolRoom, null=True)

class Computer(DistrictAsset):
    os = models.CharField(max_length=30, choices=OS_CHOICES, null=True)
    processor = models.CharField(max_length=30, null=True)
    hd_size = models.CharField(max_length=10, choices=HD_SIZE_CHOICES, null=True)
    ram = models.CharField(max_length=30, choices=RAM_SIZE_CHOICES, null=True)
    monitor_size = models.CharField(max_length=30, choices=MONITOR_SIZE_CHOICES, null=True)
    
    class Meta:
        ordering = ('school',)
        
    def __unicode__(self):
        return u"%s %s %s %s" % (self.os, self.processor, self.ram, self.hd_size)


