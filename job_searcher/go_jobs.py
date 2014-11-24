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
    # Needed to communicate with the server - NOT secret
    PASS = '02e19abe-b6f4-4a7e-bb70-9e613fcb43c2'

    def __init__(self, guid):
        """ :param guid: Needed for identification """
        self.guid = guid

    def find_results_amount(self, keyword=''):
        request_data = {'guid': self.guid,
                        "amount": 2147483647,  # Int32 maximum
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

        # The last 3 elements returned are always 0's
        job_ids = json.loads(response_search.text)['d'][:-3]
        return self.get_details_for_jobs(job_ids)

    def get_details_for_jobs(self, job_ids):
        """ Gets job details for the given job id's
        :param job_ids: Id's for the jobs, that you want to retrieve.
        :return: A list of the given jobs
        """
        jobs = []

        for job_id in job_ids:
            jobs.append(self.get_details_for_job(job_id))
        return jobs

    def get_details_for_job(self, job_id):
        """ Gets job details for the given job id
        :param job_id: Id for the job, that you want to retrieve.
        :return: A job
        """
        request_job_data = {'guid': self.guid,
                            'id': job_id,
                            'networkId': 3,
                            'pass': GoJobs.PASS}

        response_job = requests.post(self.BASE_URL +
                                     self.URL_EXTENSION_GET_JOB,
                                     data=json.dumps(request_job_data),
                                     headers=self.HEADERS)

        return GoJobs.json_to_job(response_job.text)

    @staticmethod
    def json_to_job(json_text):
        """ Converts a json string to a job
        :param json_text: The json string, that should be parsed.
        :return: A job
        """
        json_job = json.loads(json_text)['d']
        return Job(title=json_job['jobTitle'],
                   company_name=json_job['companyName'],
                   teaser=json_job['teaser'],
                   job_url='http://go.dk/job/' + str(json_job['jobId']))
