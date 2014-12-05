# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from job_searcher.go_jobs import GoJobs
from job_searcher.job import Job
import os
import responses

test_path = os.path.dirname(__file__)
job_json_path = os.path.join(test_path, 'go_jobs_test_job.json')
job_ids_json_path = os.path.join(test_path, 'go_jobs_test_job_ids.json')
job_ids_simple_json_path = \
    os.path.join(test_path, 'go_jobs_test_job_ids_simple.json')


job_json = open(job_json_path).read()
job_ids_json = open(job_ids_json_path).read()
job_ids_simple_json = open(job_ids_simple_json_path).read()
job = Job(title='Revisorer til den offentlige sektor-gruppe i EY',
          company_name='EY',
          teaser='EY er en af verdens bedste organisationer inden for '
                 'revision, skat, transaktioner og r\\u0102\\u013ddgivning. '
                 'Den indsigt og de ydelser, vi leverer, opbygger tillid '
                 'til kapitalmarkederne. Vi udvikler '
                 'dygtige ledere og medarbejdere, som sammen leverer det, '
                 'vi lover vores interessenter og bidrager til, at '
                 'arbejdsverdenen og arbejdslivet fungerer bedre - for '
                 'vores medarbejdere, vores kunder og det omgivende '
                 'samfund.',
          job_url='http://go.dk/job/572362')


@responses.activate
def test_find_results():
    responses.add(responses.POST,
                  GoJobs.BASE_URL + GoJobs.URL_EXTENSION_SEARCH,
                  body=job_ids_simple_json,
                  content_type="application/json")

    responses.add(responses.POST,
                  GoJobs.BASE_URL + GoJobs.URL_EXTENSION_GET_JOB,
                  body=job_json,
                  content_type="application/json")

    found_job = GoJobs('guid').find_results('udivkler')[0]
    assert found_job.title == job.title
    assert found_job.company_name == job.company_name
    assert found_job.teaser == job.teaser
    assert found_job.job_url == job.job_url


@responses.activate
def test_find_results_amount():
    responses.add(responses.POST,
                  GoJobs.BASE_URL + GoJobs.URL_EXTENSION_SEARCH,
                  body=job_ids_json,
                  content_type="application/json")

    assert GoJobs('guid').find_results_amount('udvikler') == 433


def test_json_to_job():
    found_job = GoJobs.json_to_job(job_json)
    assert found_job.title == job.title
    assert found_job.company_name == job.company_name
    assert found_job.teaser == job.teaser
    assert found_job.job_url == job.job_url
