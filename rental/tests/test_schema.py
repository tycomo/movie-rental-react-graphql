import pytest
from mixer.backend.django import mixer
from graphql_relay.node.node import to_global_id
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from .. import schema

pytestmark = pytest.mark.django_db

def test_movie_rental_type():
    instance = schema.MovieRentalType()
    assert instance

def test_movie_rental_all_rentals():
    mixer.blend('rental.MovieRental')
    mixer.blend('rental.MovieRental')
    q = schema.Query()
    res = q.resolve_all_rentals(None)
    assert res.count() == 2, 'Should return all movie rentals'
