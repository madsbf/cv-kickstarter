# coding=utf-8
from go_jobs import GoJobs
from job import Job
import os

test_path = os.path.dirname(__file__)
json_path = os.path.join(test_path, 'go_jobs_test_job.json')

json = open(json_path).read()
job = Job(title='Revisorer til den offentlige sektor-gruppe i EY',
          company_name='EY',
          teaser='EY er en af verdens førende organisationer inden for '
                 'revision, skat, transaktioner og rådgivning. Den indsigt '
                 'og de ydelser, vi leverer, hjælper med at opbygge tillid '
                 'til kapitalmarkederne og den globale økonomi. Vi udvikler '
                 'dygtige ledere og medarbejdere, som sammen leverer det, '
                 'vi lover vores interessenter og bidrager til, at '
                 'arbejdsverdenen og arbejdslivet fungerer bedre - for '
                 'vores medarbejdere, vores kunder og det omgivende '
                 'samfund.',
          job_url='http://go.dk/job/572362')


def test_json_to_job():
    assert GoJobs.json_to_job(json) == job
