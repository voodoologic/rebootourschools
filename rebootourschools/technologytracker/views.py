from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from technologytracker.models import *
# Create your views here.

@login_required(login_url='/login/')
def home(request):
    
    ###retrieve the district that the current user is assigned to
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    
    ###retrieve all of the schools in the user's district
    schools = School.objects.filter(district=userDistrict)
    
    
    return render_to_response('home.html', {'userDistrict': userDistrict, 'schools': schools})

@login_required(login_url='/login/')
def districtReporting(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set
    return render_to_response('districtReporting.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets})
    
@login_required(login_url='/login/')
def districts(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set
    
    ##get a list of all the districts
    districts = District.objects.all()
    
    return render_to_response('districts.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets, 'districts': districts})     
    
@login_required(login_url='/login/')
def schools(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set

    ##get a list of all the districts
    schools = School.objects.all()

    return render_to_response('schools.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets, 'schools': schools})       
    
@login_required(login_url='/login/')
def addDistrict(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set
    
    if request.method == 'POST': # If the form has been submitted...
        form = DistrictForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            
            return HttpResponseRedirect('/addDistrict/') # Redirect after POST
    else:
        form = DistrictForm() # An unbound form                
    
    return render_to_response('addDistrict.html', {
        'userDistrict': userDistrict, 
        'districtAssets': districtAssets, 
        'form': form},
         context_instance=RequestContext(request))  
    
@login_required(login_url='/login/')
def addSchool(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set

    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect('/addSchool/') # Redirect after POST
    else:
        form = SchoolForm() # An unbound form                

    return render_to_response('addSchool.html', {
        'userDistrict': userDistrict, 
        'districtAssets': districtAssets, 
        'form': form},  
        context_instance=RequestContext(request)) 
     
      

