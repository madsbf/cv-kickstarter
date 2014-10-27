from job_searcher import JobSearcher

__author__ = 'Mads'

import requests
import json

class GoJobs (JobSearcher):
    """ JobSearcher for Go.dk"""

    BASE_URL = 'http://moveon.dk/webservice/mobile.asmx/SearchJobsV3'
    HEADERS = {"Content-type": "application/json",
           "Accept": "text/plain"}
    PASS = '02e19abe-b6f4-4a7e-bb70-9e613fcb43c2' # Needed to communicate with the server

    def __init__(self, guid):
        """ :param guid: Needed for identification """
        self.guid = guid

    def find_results_amount(self, keyword=''):
        request_data = {'guid' : self.guid,
                'amount' : 2147483647, # Int32 maximum - if anything above is used, the server will respond with an error
                'text' : keyword,
                'geoIds' : [-1],
                'networkId' : 3,
                'uddIds' : [-1],
                'jobTypeIds' : [-1],
                'pass' : GoJobs.PASS}

        response = requests.post(GoJobs.BASE_URL, data=json.dumps(request_data), headers=GoJobs.HEADERS)
        response_data = json.loads(response.text)['d']
        return len(response_data)

    def find_results(self, keywords=None, amount=25):
        keywordString = ','.join(keywords)

        request_data = {'guid' : self.guid,
                'amount' : amount,
                'text' : keywordString,
                'geoIds' : [-1],
                'networkId' : 3,
                'uddIds' : [-1],
                'jobTypeIds' : [-1],
                'pass' : GoJobs.PASS}

        response = requests.post(GoJobs.BASE_URL, data=json.dumps(request_data), headers=GoJobs.HEADERS)
        response_data = json.loads(response.text)['d']
        return response_data