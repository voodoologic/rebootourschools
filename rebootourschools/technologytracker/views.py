from django.http import HttpResponse

from django.shortcuts import render_to_response

from technologytracker.models import District
# Create your views here.

def detail(request):
    #HttpResponse("Blaahhhhh!")
    return render_to_response('technologytracker/index.html', {})
