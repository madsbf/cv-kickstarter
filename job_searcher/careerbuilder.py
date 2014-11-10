from job import Job
from job_searcher import JobSearcher

__author__ = 'Mads'

import requests
from bs4 import BeautifulSoup as soup

class CareerBuilder (JobSearcher):
    """ JobSearcher for CareerBuilder.com"""

    BASE_URL = 'http://api.careerbuilder.com/v2/jobsearch'
    PARAM_DEV_KEY = 'DeveloperKey'
    PARAM_KEYWORDS = 'keywords'
    PARAM_PER_PAGE = "perpage"

    def __init__(self, developer_key):
        """ :param developer_key: Needed for identification"""

        self.developer_key = developer_key

    def find_results_amount(self, keyword=''):
        args = {self.PARAM_DEV_KEY: self.developer_key,
                self.PARAM_KEYWORDS: keyword}
        response = requests.get(self.BASE_URL, args)
        data = soup(response.text, features='xml')
        return int(data.ResponseJobSearch.TotalCount.contents[0])

    def find_results(self, keywords=[], amount=5):
        args = {self.PARAM_DEV_KEY: self.developer_key,
                self.PARAM_PER_PAGE: str(amount),
                self.PARAM_KEYWORDS: ','.join(keywords)}
        response = requests.get(self.BASE_URL, args)
        jobs = self.soup_to_jobs(soup(response.text, features='xml'))
        return jobs

    def soup_to_jobs(self, soup):
        jobs = []
        results = soup.find_all('JobSearchResult')

        for result in results:
            jobs.append(Job(title=result.JobTitle.text,
                   company_name=result.Company.text,
                   teaser=result.DescriptionTeaser.text,
                   job_url=result.JobDetailsURL.text))

        return jobs