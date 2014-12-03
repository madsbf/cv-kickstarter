""" Module for job searching. """

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

    def find_results_best_match(self, keywords=[], amount=5):
        """ Perform a job matching.

        Performs a job search for each keyword, and finds the best matching
        jobs. Uses the keyword rank, and the amount of occurrences of a given
        job to rank the jobs relevance.

        :param keywords: Keywords, that should be contained in the returned
        results.
        :param amount: The amount of results wanted.
        :return: The jobs found by the given search parameters.
        """
        all_jobs = []
        scores = []
        for keyword in keywords:
            keyword_jobs = self.find_results([keyword.keyword])
            for job in keyword_jobs:
                if(all_jobs.__contains__(job)):
                    scores[all_jobs.index(job)] += keyword.rank
                else:
                    scores.append(keyword.rank)
                    all_jobs.append(job)
        sorted_jobs = [x for (y, x) in sorted(zip(scores, all_jobs))]
        return sorted_jobs[:amount]
