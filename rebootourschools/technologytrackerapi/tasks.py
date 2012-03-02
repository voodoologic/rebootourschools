from celery.decorators import task
from technologytracker.models import District
import datetime
from technologytrackerapi.models import RunRecord

@task()
def add(x, y):
    return x + y

@task()
def createRecord():
    rr = RunRecord()
    rr.runtime = datetime.datetime.now()
    rr.save()
