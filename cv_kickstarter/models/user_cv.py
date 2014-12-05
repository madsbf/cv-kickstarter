"""UserCV for displaying the students CV on the frontend."""


class UserCV(object):

    """UserCV object works as an view object to be used in the view."""

    def __init__(self, first_name, last_name, exam_result_programmes,
                 keywords):
        """Initialize UserCV.

        Initialized with first_name, last_name and exam_result_programmes,
        keywords (skills) for the student.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.exam_result_programmes = exam_result_programmes
        self.keywords = keywords

    def course_title_sentence(self, keyword):
        """Return a course title sentence.

        If one course: 01234 Course
        For two courses: 01234 Course 1 and 01235 Course 2
        For three courses: 01234 C1, 01235 C2 and 012346 C3
        """
        return self._to_sentence(
            list(map(lambda x: x.title, keyword.course_numbers))
        )

    @property
    def highest_ranked_keywords(self):
        """Return the 50 highest ranked keywords."""
        return self.keywords[:50]

    @property
    def full_name(self):
        """Return the full name of the student."""
        return " ".join([self.first_name, self.last_name])

    def _to_sentence(self, list_of_words):
        if len(list_of_words) <= 1:
            return list_of_words[0]
        elif len(list_of_words) == 2:
            return " and ".join(list_of_words)
        else:
            return " and ".join(
                [", ".join(list_of_words[0:-1]), list_of_words[-1]]
            )
