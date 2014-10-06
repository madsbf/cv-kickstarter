__author__ = 'Mads'

import requests
import json

data = {'guid' : '70498191-2018-4788-b7a3-f2973b8a178c',
        'amount' : 2147483647, # Int32 maximum - if anything above is used, the server will respond with an error
        'text' : 'udvikler',
        'geoIds' : [-1],
        'networkId' : 3,
        'uddIds' : [-1],
        'jobTypeIds' : [-1],
        'pass' : '02e19abe-b6f4-4a7e-bb70-9e613fcb43c2'}

headers = {"Content-type": "application/json",
           "Accept": "text/plain"}

url = 'http://moveon.dk/webservice/mobile.asmx/SearchJobsV3'

response = requests.post(url, data=json.dumps(data), headers=headers)
print response.text