from technologytracker.models import School
from technologytracker.models import Computer
from technologytracker.models import LicensedSoftware
from technologytracker.models import Printer
from technologytracker.models import Tablet
from technologytracker.models import MobileDevice
from technologytracker.models import District
from django.contrib import admin

class SchoolsInline(admin.TabularInline):
    model = School
    extra = 1

class ComputersInline(admin.TabularInline):
    model = Computer
    extra = 1
    
class LicensedSoftwaresInline(admin.TabularInline):
    model = LicensedSoftware
    extra = 1

class PrintersInline(admin.TabularInline):
    model = Printer
    extra = 1

class TabletsInline(admin.TabularInline):
    model = Tablet
    extra = 1    
            
class MobileDevicesInline(admin.TabularInline):
    model = Tablet
    extra = 1        

class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        ('School info', {'fields' : ['full_name', 'school_code', 'district']})
        
    ]
    list_display = ('full_name', 'school_code', 'district')
    list_filter = ['district',]
    search_fields = ['full_name', 'school_code']
    inlines = [ComputersInline, LicensedSoftwaresInline, PrintersInline, TabletsInline, MobileDevicesInline]
    
class DistrictAdmin(admin.ModelAdmin):
    fieldsets = [
        ('District info', {'fields' : ['full_name', 'district_code', 'city', 'state', 'county']})
        
    ]
    list_display = ('full_name', 'district_code', 'city', 'state', 'county')
    list_filter = ['district_code']
    search_fields = ['full_name', 'district_code', 'city', 'state', 'county']
    inlines = [SchoolsInline]
            

admin.site.register(School, SchoolAdmin)
admin.site.register(District, DistrictAdmin)


