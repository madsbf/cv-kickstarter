__author__ = 'Mads'

class JobSearcher:
    """ The JobSearcher allows finding jobs for a given keyword, or just finding the amount of results for a given
    keyword """

    def find_results_amount(self, keyword=''):
        """Finds the amount of results for a given keyword """
        raise NotImplementedError

    def find_results(self, keywords=None, amount=5):
        """ Performs a job search
        :param keywords: Keywords, that should be contained in the returned results
        :param amount: The amount of results wanted
        :return: The jobs found by the given search parameters
        """
        raise NotImplementedError