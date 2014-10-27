__author__ = 'Mads'


class KeywordEvaluator:

    def __init__(self, job_searcher):
        self.job_searcher = job_searcher

    def evaluate_keyword(self, keyword):
        totalJobs = self.job_searcher.find_results_amount("")
        keywordJobs = self.job_searcher.find_results_amount(keyword)
        return keywordJobs / totalJobs * 100