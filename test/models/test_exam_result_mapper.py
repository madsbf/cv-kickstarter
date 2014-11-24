from cv_kickstarter.model.campus_net_exam_result_mapper import (
  CampusNetExamResultMapper, ExamResultProgramme
)
from mock import Mock, MagicMock
from collections import namedtuple
from pytest import yield_fixture

result_double = namedtuple('ExamResult',
                           ['name', 'passed_ects_points', 'exam_results'])


@yield_fixture
def map_init(monkeypatch):
    exam_result_init = Mock(return_value=None)
    monkeypatch.setattr(ExamResultProgramme, '__init__', exam_result_init)
    yield exam_result_init


def test_mapped_result_returns_exam_result_for_bachelor_programme(monkeypatch,
                                                                  map_init):
    exam_results = MagicMock()
    exam_result_programme = result_double('Bachelor (Softwaretechnology)',
                                          65.0,
                                          exam_results)
    CampusNetExamResultMapper(exam_result_programme).mapped_exam_result()
    map_init.assert_called_with('Bachelor (Softwaretechnology)',
                                65.0,
                                180.0,
                                exam_results)


def test_mapped_result_returns_exam_result_for_master_programme(monkeypatch,
                                                                map_init):
    exam_results = MagicMock()
    exam_result_programme = result_double('Master (Informationtechonology)',
                                          75.0,
                                          exam_results)
    CampusNetExamResultMapper(exam_result_programme).mapped_exam_result()
    map_init.assert_called_with('Master (Informationtechonology)',
                                75.0,
                                120.0,
                                exam_results)


def test_mapped_result_returns_exam_result_programme():
    exam_results = MagicMock()
    exam_result_programme = result_double('Master (Informationtechonology)',
                                          75.0,
                                          exam_results)
    mapped_exam_result = CampusNetExamResultMapper(
        exam_result_programme
    ).mapped_exam_result()
    assert type(mapped_exam_result) == ExamResultProgramme
