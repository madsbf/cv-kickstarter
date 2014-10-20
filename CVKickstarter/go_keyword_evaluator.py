__author__ = 'Mads'

import requests
import json

class GoKeywordEvaluator:
    BASE_URL = 'http://moveon.dk/webservice/mobile.asmx/SearchJobsV3'
    HEADERS = {"Content-type": "application/json",
           "Accept": "text/plain"}
    PASS = '02e19abe-b6f4-4a7e-bb70-9e613fcb43c2' # Pass, that is needed to communicate with the server
    GUID = '70498191-2018-4788-b7a3-f2973b8a178c' # Fake GUID, that lets us get data from the server

    @staticmethod
    def find_results_amount(keyword):
        request_data = {'guid' : GoKeywordEvaluator.GUID,
                'amount' : 2147483647, # Int32 maximum - if anything above is used, the server will respond with an error
                'text' : keyword,
                'geoIds' : [-1],
                'networkId' : 3,
                'uddIds' : [-1],
                'jobTypeIds' : [-1],
                'pass' : GoKeywordEvaluator.PASS}

        response = requests.post(GoKeywordEvaluator.BASE_URL, data=json.dumps(request_data), headers=GoKeywordEvaluator.HEADERS)
        response_data = json.loads(response.text)['d']
        return len(response_data)

    @staticmethod
    def find_results(keywords, amount):
        keywordString = keywords[0]
        for keyword in keywords:
            keywordString += keyword + ", "

        request_data = {'guid' : GoKeywordEvaluator.GUID,
                'amount' : amount,
                'text' : keywordString,
                'geoIds' : [-1],
                'networkId' : 3,
                'uddIds' : [-1],
                'jobTypeIds' : [-1],
                'pass' : GoKeywordEvaluator.PASS}

        response = requests.post(GoKeywordEvaluator.BASE_URL, data=json.dumps(request_data), headers=GoKeywordEvaluator.HEADERS)
        response_data = json.loads(response.text)['d']
        return response_data

print GoKeywordEvaluator.find_results_amount('udvikler')
print GoKeywordEvaluator.find_results(['udvikler', 'konge'], 25)