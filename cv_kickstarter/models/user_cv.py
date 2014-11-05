class UserCV(object):
    def __init__(self, first_name, last_name, exam_result_programmes,
                 keywords):
        self.first_name = first_name
        self.last_name = last_name
        self.exam_result_programmes = exam_result_programmes
        self.keywords = keywords

    @property
    def highest_ranked_keywords(self):
        return self.keywords[:10]

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])
