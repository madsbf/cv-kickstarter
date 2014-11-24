__author__ = 'Mads'


class Job:
    """ Simple job class, used to expose a generic interface for jobs
    across different job searchers"""

    def __init__(self, title, company_name, teaser, job_url):
        self.title = title
        self.company_name = company_name
        self.teaser = teaser
        self.job_url = job_url
