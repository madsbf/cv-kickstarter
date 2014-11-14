class UserCV(object):
    def __init__(self, first_name, last_name, exam_result_programmes,
                 keywords):
        self.first_name = first_name
        self.last_name = last_name
        self.exam_result_programmes = exam_result_programmes
        self.keywords = keywords

    def to_sentence(self, list_of_words):
        if len(list_of_words) <= 1:
            return list_of_words[0]
        elif len(list_of_words) == 2:
            return " and ".join(list_of_words)
        else:
            return " and ".join(
                [", ".join(list_of_words[0:-1]), list_of_words[-1]]
            )

    def course_title_sentence(self, keyword):
        return self.to_sentence(
            map(lambda x: x.title, keyword.course_numbers)
        )

    @property
    def highest_ranked_keywords(self):
        return self.keywords[:50]

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])
