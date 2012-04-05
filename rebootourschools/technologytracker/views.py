from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from GChartWrapper import *


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
        
        
        if request.method == 'POST':
            form = SchoolForm(request.POST)
            if form.is_valid():
                form.save()

                return HttpResponseRedirect('/addSchool/') # Redirect after POST
        else:
            form = SchoolForm() # An unbound form
         
        return render_to_response('home.html', {'userDistrict': userDistrict, 'schools': schools, 'schoolCount':schoolCount, 'form':form})
    
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
         
         
         ##os chart
         osxCount = Computer.objects.filter(school=school, os='OSX').count()
         linuxCount = Computer.objects.filter(school=school, os='LINUX').count()
         windowsCount = Computer.objects.filter(school=school, os='WINDOWS').count()
         
         osDataset = [osxCount, linuxCount, windowsCount]
         osChart = Pie3D( osDataset )
         osChart.label('OS X','LINUX','WINDOWS')
         osChart.color('4d89f9','c6d9fd')
         osChart.title('Operating Systems')
         
         ##hd chart
         smallHd = Computer.objects.filter(school=school, hd_size='60').count()
         mediumHd = Computer.objects.filter(school=school, hd_size='128').count()
         largeHd = Computer.objects.filter(school=school, hd_size='250').count()

         hdDataset = [smallHd, mediumHd, largeHd]
         hdChart = Pie3D( hdDataset )
         hdChart.label('60 GB','128 GB','250GB')
         hdChart.color('4d89f9','c6d9fd')
         hdChart.title('Memory (Hard Drives)')
         
         ##ram chart
         oneGb = Computer.objects.filter(school=school, ram='1').count()
         twoGb = Computer.objects.filter(school=school, ram='2').count()
         fourGb = Computer.objects.filter(school=school, ram='4').count()
         eightGb = Computer.objects.filter(school=school, ram='8').count() 

         ramDataset = [oneGb, twoGb, fourGb, eightGb]
         ramChart = Pie3D( ramDataset )
         ramChart.label('1 GB','2 GB','4 GB', '8 GB')
         ramChart.color('4d89f9','c6d9fd')
         ramChart.title('Memory (RAM)') 
         
         return render_to_response('schoolDetail.html', {'school':school, 
            'computers':computers, 
            'computerCount':computerCount,
            'osxCount':osxCount,
            'linuxCount':linuxCount,
            'windowsCount':windowsCount,
            'form':form,
            'osChart':osChart,
            'hdChart':hdChart,
            'ramChart':ramChart,
            })
     
     except School.DoesNotExist:        
         return HttpResponseNotFound('School not found')


@login_required(login_url='/login/')
def districtReporting(request):
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    districtAssets = userDistrict.districtasset_set
    
    ###retrieve the district that the current user is assigned to
    districtUserProfile = DistrictUserProfile.objects.filter(user=request.user)
    userDistrict = District.objects.get(pk=districtUserProfile)
    
    ###retrieve all of the schools in the user's district
    schools = School.objects.filter(district=userDistrict)
    schoolCount = School.objects.filter(district=userDistrict).count()
    
    schoolDataset = []
    schoolLabels = []
    for school in schools:
        schoolLabels.append(school.full_name)
        computerCount = Computer.objects.filter(school=school).count()
        schoolDataset.append(computerCount)

        computerCountChart = VerticalBarStack(schoolDataset)
        #computerCountChart.label(schoolLabels)
        computerCountChart.color('4d89f9','c6d9fd')
        computerCountChart.title('Count by school')
        computerCountChart.size(600,375)
        
    horizontalBarStack = HorizontalBarStack(['hello','world'], encoding='simple')
    horizontalBarStack.color('4d89f9','c6d9fd')
    horizontalBarStack.title('Memory')
    horizontalBarStack.size(400,250)    
    horizontalBarStack.label('1 GB','2 GB','4 GB', '8 GB')
    
    verticalBarGroup = VerticalBarGroup(['hello','world'], encoding='simple')
    verticalBarGroup.color('4d89f9','c6d9fd')
    verticalBarGroup.size(400,250)
    
    meter = Meter(10)
    meter.label('10th Percentile')
    meter.size(400,200)
    
    verticalBarStack = VerticalBarStack([ [30,25,26,10,20],[50,60,80,40,20] ], encoding='text')
    verticalBarStack.color('4d89f9', 'c6d9fd')
    verticalBarStack.size(400,200)
    
    return render_to_response('districtReporting.html', {
        'userDistrict': userDistrict, 
        'districtAssets': districtAssets, 
        'schools': schools,
        'schoolCount': schoolCount,
        'computerCountChart': computerCountChart,
        'horizontalBarStack': horizontalBarStack,
        'verticalBarGroup': verticalBarGroup,
        'meter': meter,
        'verticalBarStack': verticalBarStack,
    })
    
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
     
      

