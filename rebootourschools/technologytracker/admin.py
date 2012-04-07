from technologytracker.models import School, Computer, Tablet, District, DistrictUserProfile
from django.contrib import admin

class SchoolsInline(admin.TabularInline):
    model = School
    extra = 1

class ComputersInline(admin.TabularInline):
    model = Computer
    extra = 1
    
class TabletsInline(admin.TabularInline):
    model = Tablet
    extra = 1    
            
class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        ('School info', {'fields' : ['full_name', 'school_code', 'district']})      
    ]
    list_display = ('full_name', 'school_code', 'district')
    list_filter = ['district',]
    search_fields = ['full_name', 'school_code']

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
admin.site.register(DistrictUserProfile)


