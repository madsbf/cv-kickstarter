""" Generic job module. """


class Job:

    """ Generic Job interface.

    Simple job class, used to expose a generic interface for jobs
    across different job searchers.
    """

    def __init__(self, title, company_name, teaser, job_url):
        """ Initialize a Job.

        :param title: The job title.
        :param company_name: The name of the company offering the job.
        :param teaser: A short teaser text for the job.
        :param_teaser: An external URL providing further info about the job.
        """
        self.title = title
        self.company_name = company_name
        self.teaser = teaser
        self.job_url = job_url
