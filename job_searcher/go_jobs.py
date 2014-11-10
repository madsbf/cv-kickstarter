from job import Job
from job_searcher import JobSearcher

__author__ = 'Mads'

import requests
import json


class GoJobs (JobSearcher):
    """ JobSearcher for Go.dk"""

    BASE_URL = 'http://moveon.dk/webservice/mobile.asmx/'
    URL_EXTENSION_SEARCH = 'SearchJobsV3'
    URL_EXTENSION_GET_JOB = "GetJobLimitedV3"

    HEADERS = {"Content-type": "application/json",
               "Accept": "text/plain"}
    PASS = '02e19abe-b6f4-4a7e-bb70-9e613fcb43c2'  # Needed to communicate with the server - NOT secret

    def __init__(self, guid):
        """ :param guid: Needed for identification """
        self.guid = guid

    def find_results_amount(self, keyword=''):
        request_data = {'guid': self.guid,
                        "amount": 2147483647,  # Int32 maximum - Anything above will result in a server error
                        'text': keyword,
                        'geoIds': [-1],
                        'networkId': 3,
                        'uddIds': [-1],
                        'jobTypeIds': [-1],
                        'pass': GoJobs.PASS}

        response = requests.post(GoJobs.BASE_URL,
                                 data=json.dumps(request_data),
                                 headers=GoJobs.HEADERS)
        response_data = json.loads(response.text)['d']
        return len(response_data)

    def find_results(self, keywords=(), amount=5):
        request_search_data = {'guid': self.guid,
                               'amount': amount,
                               'text': ','.join(keywords),
                               'geoIds': [-1],
                               'networkId': 3,
                               'uddIds': [-1],
                               'jobTypeIds': [-1],
                               'pass': GoJobs.PASS}

        response_search = requests.post(self.BASE_URL +
                                        self.URL_EXTENSION_SEARCH,
                                        data=json.dumps(request_search_data),
                                        headers=self.HEADERS)
        job_ids = json.loads(response_search.text)['d'][:-3]  # The last 3 elements returned are always 0's
        jobs = []

        for job_id in job_ids:
            request_job_data = {'guid': self.guid,
                                'id': job_id,
                                'networkId': 3,
                                'pass': GoJobs.PASS}

            response_job = requests.post(self.BASE_URL +
                                         self.URL_EXTENSION_GET_JOB,
                                         data=json.dumps(request_job_data),
                                         headers=self.HEADERS)
            jobs.append(self.json_to_job(response_job.text))

        return jobs

    @staticmethod
    def json_to_job(json_text):
        json_job = json.loads(json_text)['d']
        return Job(title=json_job['jobTitle'],
                   company_name=json_job['companyName'],
                   teaser=json_job['teaser'],
                   job_url='http://go.dk/job/' + str(json_job['jobId']))