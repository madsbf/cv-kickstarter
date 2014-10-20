# -*- coding: utf-8 -*-

import dtu_course_base
import re


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
