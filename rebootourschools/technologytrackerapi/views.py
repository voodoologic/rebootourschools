from django.shortcuts import render_to_response

from djcelery.schedulers import ModelEntry, DatabaseScheduler
from djcelery.models import IntervalSchedule, PeriodicTask
from celery.schedules import schedule, timedelta

from .models import RunRecord 
from .tasks import createRecord
# Create your views here.


def taskViewer(request):
    return render_to_response('taskView.html')

def addTask(request):

    intervalSchedule = IntervalSchedule.from_schedule(schedule(timedelta(seconds=10)))
    intervalSchedule.save()
    modelData = dict(
        name="dcTestPersist",
        task="technologytrackerapi.tasks.createRecord",
        interval_id=intervalSchedule.pk,
    )
    periodicTask = PeriodicTask(**modelData)
    periodicTask.save()
#    return periodicTask
#    n = periodicTask.name
    me = ModelEntry(periodicTask)
    try:
        me.save()
    except:
      from django.db import connection
      print connection.queries
      raise
#    return me
    return render_to_response('taskView.html')
