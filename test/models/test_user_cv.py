import sys
sys.path.append('cv_kickstarter/models')

from user_cv import UserCV


def test_full_name_from_first_and_last_name():
    user_cv = UserCV('Donald', 'Duck', [], [])
    assert user_cv.full_name == 'Donald Duck'
