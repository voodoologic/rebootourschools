from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


from technologytracker.models import *
# Create your views here.

def splash(request):
    return render_to_response('splash.html')


@login_required(login_url='/login/')
def home(request):
    
    try:
        ###retrieve the district that the current user is assigned to
        districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
        userDistrict = District.objects.get(pk=districtUserProfile)
        
        ###retrieve all of the schools in the user's district
        schools = School.objects.filter(district=userDistrict)
        schoolCount = School.objects.filter(district=userDistrict).count()
        
        return render_to_response('home.html',
                                  {'userDistrict': userDistrict, 'schools': schools, 'schoolCount':schoolCount},
                                  context_instance=RequestContext(request))
    
    ###exceptions
    except DistrictUserProfile.DoesNotExist:
        return HttpResponseNotFound('District profile not found')
    except District.DoesNotExist:
        return HttpResponseNotFound('District not found')
    except School.DoesNotExist:        
        return HttpResponseNotFound('School not found')     


@login_required(login_url='/login/')    
def schoolDetail(request, school_id):
     
     try:
         school = School.objects.get(pk=school_id)
         computers = Computer.objects.filter(school=school).order_by('os', 'ram')
         computerCount = Computer.objects.filter(school=school).count()
         osxCount = Computer.objects.filter(school=school, os='OSX').count()
         linuxCount = Computer.objects.filter(school=school, os='LINUX').count()
         windowsCount = Computer.objects.filter(school=school, os='WINDOWS').count()
         
         if request.method == 'POST':
             form = ComputerForm(request.POST)
             if form.is_valid():
                 form.save()

                 return HttpResponseRedirect('/addComputer/') # Redirect after POST
         else:
             form = ComputerForm() # An unbound form
         
         
         return render_to_response('schoolDetail.html', {'school':school, 
            'computers':computers, 
            'computerCount':computerCount,
            'osxCount':osxCount,
            'linuxCount':linuxCount,
            'windowsCount':windowsCount,
            'form':form})
     
     except School.DoesNotExist:        
         return HttpResponseNotFound('School not found')


@login_required(login_url='/login/')
def districtReporting(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    districtAssets = userDistrict.districtasset_set
    return render_to_response('districtReporting.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets})


@login_required(login_url='/login/')
def districts(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    districtAssets = userDistrict.districtasset_set
    
    ##get a list of all the districts
    districts = District.objects.all()
    
    return render_to_response('districts.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets, 'districts': districts})     


@login_required(login_url='/login/')
def schools(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    districtAssets = userDistrict.districtasset_set

    ##get a list of all the districts
    schools = School.objects.all()

    return render_to_response('schools.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets, 'schools': schools})       


@login_required(login_url='/login/')
def addDistrict(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
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
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    districtAssets = userDistrict.districtasset_set

    if request.method == 'POST':
        school=School(district=userDistrict,
                      full_name=request.POST['schoolName'],
                      school_code=request.POST['schoolCode'])
        school.save()
        return HttpResponseRedirect('/schools/') # Redirect after POST
    else:
        form = SchoolForm() # An unbound form                

    return render_to_response('addSchool.html', {
        'userDistrict': userDistrict, 
        'districtAssets': districtAssets, 
        'form': form},  
        context_instance=RequestContext(request)) 


@login_required(login_url='/login/')
def addComputer(request):

    if request.method == 'POST':
        form = ComputerForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/addComputer/') # Redirect after POST
    else:
        form = ComputerForm() # An unbound form                

    return render_to_response('addComputer.html', { 
        'form': form},  
        context_instance=RequestContext(request))        



