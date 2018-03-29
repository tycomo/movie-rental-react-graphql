import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

def test_message():
    obj = mixer.blend('rental.MovieRental')
    assert obj.pk > 0

