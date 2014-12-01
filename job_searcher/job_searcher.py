""" Module for job searching. """

__author__ = 'Mads'


class JobSearcher:

    """ Class for job searching.

    JobSearcher finds jobs for a given keyword, or just
    find the amount of jobs for a given keyword.
    """

    def find_results_amount(self, keyword=''):
        """Find the amount of results for a given keyword. """
        raise NotImplementedError

    def find_results(self, keywords=(), amount=5):
        """ Perform a job search.

        :param keywords: Keywords, that should be contained in the returned
        results.
        :param amount: The amount of results wanted.
        :return: The jobs found by the given search parameters.
        """
        raise NotImplementedError
