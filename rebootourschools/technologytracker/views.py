from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson

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
         
         return render_to_response('schoolDetail.html',
                                   {'school':school,
                                    'computers':computers,
                                    'computerCount':computerCount,
                                    'osxCount':osxCount,
                                    'linuxCount':linuxCount,
                                    'windowsCount':windowsCount,
                                    'hdChoices':HD_SIZE_CHOICES,
                                    'ramChoices':RAM_SIZE_CHOICES,
                                    'osChoices':OS_CHOICES, },
                                    context_instance=RequestContext(request))
     
     except School.DoesNotExist:        
         return HttpResponseNotFound('School not found')


@login_required(login_url='/login/')    
def schooljson(request, school_pk):

    try:

        ###retrieve the district that the current user is assigned to
        districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
        userDistrict = District.objects.get(pk=districtUserProfile)

        school = School.objects.get(pk=school_pk, district=userDistrict)

        data = { 'school_name': school.full_name,
                 'school_code': school.school_code,
                 'school_type': school.school_type,
                 'school_pk': school.pk, }

        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    except School.DoesNotExist:

        return HttpResponseNotFound('School not found')


@login_required(login_url='/login/')    
def computerjson(request, computer_pk):

    try:

        ###retrieve the district that the current user is assigned to
        districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
        userDistrict = District.objects.get(pk=districtUserProfile)

        computer = Computer.objects.get(pk=computer_pk, district=userDistrict)

        data = { 'computer_school': computer.school.pk,
                 'computer_pk': computer.pk,
                 'computer_hd_size': computer.hd_size,
                 'computer_monitor_size': computer.monitor_size,
                 'computer_processor': computer.processor,
                 'computer_ram': computer.ram,
                 'computer_os': computer.os, }

        return HttpResponse(simplejson.dumps(data), content_type='application/json')

    except School.DoesNotExist:

        return HttpResponseNotFound('Computer not found')


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

    schoolTypes = School.SCHOOL_TYPE_CHOICES

    return render_to_response('schools.html',
                              {'userDistrict': userDistrict, 
                               'districtAssets': districtAssets, 
                               'schoolTypes': schoolTypes, 
                               'schools': schools},
                              context_instance=RequestContext(request) )


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

        if request.POST['schoolPk']:
            try:

                school = School.objects.get(pk=request.POST['schoolPk'], district=userDistrict)
                school.full_name = request.POST['schoolName']
                school.school_code = request.POST['schoolCode']
                school.school_type = request.POST['schoolType']
                school.save()
            except School.DoesNotExist:

                return HttpResponseNotFound('School not found')
        else:
            school=School(district=userDistrict,
                          full_name=request.POST['schoolName'],
                          school_code=request.POST['schoolCode'], )
            school.school_type = request.POST['schoolType']
            school.save()

        return HttpResponseRedirect('/schools/') # Redirect after POST

    schoolTypes = School.SCHOOL_TYPE_CHOICES

    return render_to_response('addSchool.html',
                              {'userDistrict': userDistrict,
                               'districtAssets': districtAssets, 
                               'schoolTypes': schoolTypes, },
                              context_instance=RequestContext(request)) 


@login_required(login_url='/login/')
def deleteSchool(request, school_pk):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)

    try:
        school = School.objects.get(pk=school_pk, district=userDistrict)
        school.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except School.DoesNotExist:
        return HttpResponseNotFound('School not found')


@login_required(login_url='/login/')
def addComputer(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)

    if request.method == 'POST':

        if request.POST['computerPk']:
            try:

                computer = Computer.objects.get(pk=request.POST['computerPk'], district=userDistrict)
                computer.os=request.POST['computerOS']
                computer.processor=request.POST['computerProcessor']
                computer.hd_size=request.POST['hdSize']
                computer.ram=request.POST['ram']
                computer.save()
            except Computer.DoesNotExist:

                return HttpResponseNotFound('Computer not found')
        else:
            for i in range(int(request.POST['numberOfComputers'])):

                computer=Computer(district=userDistrict,
                                  school=School.objects.get(pk=request.POST['schoolPk']),
                                  os=request.POST['computerOS'],
                                  processor=request.POST['computerProcessor'],
                                  hd_size=request.POST['hdSize'],
                                  ram=request.POST['ram'],)
                computer.save()

        return HttpResponseRedirect('/school/' + request.POST['schoolPk'] + '/') # Redirect after POST

    return render_to_response('addComputer.html', 
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def deleteComputer(request, computer_pk):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)

    try:
        computer = Computer.objects.get(pk=computer_pk, district=userDistrict)
        computer.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    except Computer.DoesNotExist:
        return HttpResponseNotFound('Computer not found')

