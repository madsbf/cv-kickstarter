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


def test_course_number_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    assert first_course.course_number == '01005'


def test_title_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    assert first_course.title == 'Matematik 1'


def test_content_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    exp_text = u"Lineære ligninger og lineære afbildninger. Matrixalgebra."
    assert first_course.contents == exp_text


def test_course_objectives_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    exp_text = u"Kursets emner udgør det matematiske grundlag for en lang..."
    assert first_course.course_objectives_text == exp_text


def test_objective_keyword_extraction():
    courses_xml = open('small_courses.xml').read()
    courses = dtu_course_base.courses_from_xml(courses_xml)
    first_course = courses[0]
    assert first_course.course_objectives == expected_course_objectives
