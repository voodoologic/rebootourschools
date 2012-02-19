from django.http import HttpResponse

from django.shortcuts import render_to_response

from technologytracker.models import District
# Create your views here.

def districtDetail(request):
    #HttpResponse("Blaahhhhh!")
    userDistrict = District.objects.get(pk=1)
    return render_to_response('technologytracker/districtDetail.html', {'userDistrict': userDistrict})
