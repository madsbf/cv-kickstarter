# -*- coding: utf-8 -*-

import dtu_course_base


expected_course_objectives = [
    u"Benytte den algebraiske og den geometriske repræsentation af de...",
    u"Benytte matrixregning og Gausselimination i forbindelse med løsning...",
    u"Analysere og forklare løsningsmængder i vektorrum ud fra...",
    u"Kunne udføre simple beregninger med de elementære funktioner,",
    u"Benytte de forskellige varianter af Taylors formel til...",
    u"Kunne løse simple første og anden ordens differentialligninger...",
    u"Beregne ekstrema for funktioner af flere variable, herunder på områder.",
    u"Kunne parametrisere simple kurver, flader og  rumlige områder, samt...",
    u"Kunne anvende Gauss' og Stokes sætninger i simple sammenhænge.",
    u"Kunne anvende matematisk terminologi og ræsonnement i forbindelse med..",
    u"Organisere samarbejdet i en projektgruppe omkring  matematiske...",
    u"Benytte symbolske software-værktøjer, for tiden Maple, til løsning..."
]


def first_course(language):
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml, language)
    return courses[0]


# Danish version
def test_danish_course_number_extraction():
    assert first_course('da-DK').course_number == '01005'


def test_danish_title_extraction():
    assert first_course('da-DK').title == 'Matematik 1'


def test_danish_content_extraction():
    exp_text = u"Lineære ligninger og lineære afbildninger. Matrixalgebra."
    assert first_course('da-DK').contents == exp_text


def test_danish_course_objectives_extraction():
    exp_text = u"Kursets emner udgør det matematiske grundlag for en lang..."
    assert first_course('da-DK').course_objectives_text == exp_text


def test_danish_objective_keyword_extraction():
    assert(
        first_course('da-DK').course_objectives == expected_course_objectives
    )


# English version
def test_english_course_number_extraction():
    assert first_course('en-GB').course_number == '01005'


def test_english_title_extraction():
    assert first_course('en-GB').title == 'Advanced Engineering Mathematics 1'


def test_english_content_extraction():
    exp_text = u"Linear equations and linear maps. Matrix algebra."
    assert first_course('en-GB').contents == exp_text


def test_english_course_objectives_extraction():
    exp_text = u"The course content is the mathematical basis for a broad..."
    assert first_course('en-GB').course_objectives_text == exp_text


def test_english_objective_keyword_extraction():
    expected_course_objectives = ["See the Danish version"
                                  for _ in range(0, 12)]
    assert(
        first_course('en-GB').course_objectives == expected_course_objectives
    )
