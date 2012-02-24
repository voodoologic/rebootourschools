from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from django.shortcuts import render_to_response

from technologytracker.models import District, DistrictUserProfile
# Create your views here.

@login_required(login_url='/techtracker/login/')
# @user_passes_test(lambda u: isinstance(u, DistrictUserProfile), login_url='/techtracker/login/')
def districtDetail(request):
    userDistrict = District.objects.get(pk=1)
    return render_to_response('districtDetail.html', {'userDistrict': userDistrict})

@login_required(login_url='/techtracker/login/')
def districtReporting(request):
    userDistrict = District.objects.get(pk=1)
    districtAssets = userDistrict.districtasset_set
    return render_to_response('districtReporting.html', {'userDistrict': userDistrict, 'districtAssets': districtAssets})

