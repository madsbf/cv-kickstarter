""" A module used for keyword evalution. """

from __future__ import division

class KeywordEvaluator:


    """ A class used to evaluate keywords with a given job searcher. """

    def __init__(self, job_searcher):
        """ Initialize a KeywordEvaluator.

        :param job_searcher: The JobSearcher used for keyword evaluation.
        """
        self.job_searcher = job_searcher

    def evaluate_keyword(self, keyword):
        """ Evaluate a keyword for the given job searcher.

        :param keyword: The keyword to evaluate.
        :return: The percentage of jobs, that contain the given keyword.
        """
        total_jobs = self.job_searcher.find_results_amount()
        keyword_jobs = self.job_searcher.find_results_amount(keyword)
        return keyword_jobs / total_jobs * 100
