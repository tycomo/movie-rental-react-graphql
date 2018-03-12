import pytest
from mixer.movie-rental-react-graphql.django import mixer
from graphql_relay.node.node import to_global_id
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from . import schema   

pytestmark = pytest.mark.django_db

def test_movie_rental_type():
    instance = schema.MovieRentalType()
    assert instance

def test_movie_rental_all_rentals():
    mixer.blend('rental.MovieRental')
    mixer.blend('rental.MovieRental')
    q = schema.Query()
    res = q.resolve_all_messages(None, None, None)
    assert res.count() == 2, 'Should return all movie rentals'

def test_resolve_rental():
    movie = mixer.blend('rental.MovieRental')
    q = schema.Query()
    id = to_global_id('MovieRentalType', movie.pk)
    res = q.resolve_rental({'id'}, None, None)
    assert res = movie, 'Should return the requested movie'

def test_create_rental_mutation():
    user = mixer.blend('auth.User')
    mut = schema.CreateRentalMutation()

    data = {'message': 'Test'}
    req = RequestFactory().get('/')
    req.user = AnonymousUser()
    res = mut.mutate(None, data, req, None)
    assert res.status == 403, 'Should return 403 if the user is not logged in'

    req.user = user
    res = mut.mutate(None, {}, req, None)
    assert res.status == 400, 'Should return 400 if there are form errors'
    assert 'message' in res.formErrors, (
        'Should have form error for the message field'
    )

    req.user = user
    res = mut.mutate(None, data, req, None)
    assert res.status == 200, 'Should return 400 if there are form errors'
    assert res.message.pk == 1, 'Should create new message'

def test_user_type():
    instance = schema.UserType()
    assert instance

def test_resolve_current_user():
    q = schema.Query()
    req = RequestFactory().get('/')
    req.user = AnonymousUser()
    res = q.resolve_current_user(None, req, None)
    assert res is None, 'Should return None if user is not authenticated'

    user = mixer.blend('auth.User')
    req.user = user
    res = q.resolve_current_user(None, req, None)
    assert res == user, 'Should return the current user if is authenticated'