""" Module for job searching on CareerBuilder.com. """

from job import Job
from job_searcher import JobSearcher

import requests
import collections
from bs4 import BeautifulSoup


class CareerBuilder (JobSearcher):

    """ JobSearcher for CareerBuilder.com. """

    BASE_URL = 'http://api.careerbuilder.com/v2/jobsearch'
    PARAM_DEV_KEY = 'DeveloperKey'
    PARAM_KEYWORDS = 'keywords'
    PARAM_PER_PAGE = "perpage"

    def __init__(self, developer_key):
        """ :param developer_key: Needed for identification. """
        self.developer_key = developer_key

    def find_results_amount(self, keyword=''):
        """Find the amount of results for a given keyword. """
        args = {self.PARAM_DEV_KEY: self.developer_key,
                self.PARAM_KEYWORDS: keyword}
        response = requests.get(self.BASE_URL, params=args)
        data = BeautifulSoup(response.text, features='xml')
        return int(data.ResponseJobSearch.TotalCount.contents[0])

    def find_results(self, keywords=[], amount=5):
        """ Perform a job search.

        :param keywords: Keywords, that should be contained in the returned
        results.
        :param amount: The amount of results wanted.
        :return: The jobs found by the given search parameters.
        """
        args = {self.PARAM_DEV_KEY: self.developer_key,
                self.PARAM_PER_PAGE: str(amount),
                self.PARAM_KEYWORDS: ','.join(keywords)}
        response = requests.get(self.BASE_URL, params=args)
        jobs = self.xml_to_jobs(response.text)
        return jobs

    @staticmethod
    def xml_to_jobs(xml):
        """ Convert xml to a list of jobs.

        :param xml: The xml string, that should be parsed.
        :return: A list of jobs.
        """
        soup = BeautifulSoup(xml, features='xml')
        results = soup.find_all('JobSearchResult')

        jobs = []
        for result in results:
            jobs.append(Job(title=result.JobTitle.text,
                            company_name=result.Company.text,
                            teaser=result.DescriptionTeaser.text,
                            job_url=result.JobDetailsURL.text))

        return jobs
