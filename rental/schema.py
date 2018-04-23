from collections import namedtuple
import graphene
import graphql_jwt
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

import json
import requests
import datetime

from django.contrib.auth import get_user_model

from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from . import models


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)


def get_popular_movies():
    if 'popular_movies' in cache:
        popular_movies = cache.get('popular_movies')
        return json2obj(json.dumps(popular_movies))
    else:
        popular = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=8879bf0d7d0370ed12d9245c5c774ae1&language=en-US&page=1')
        content = json.loads(popular.content)['results']
        cache.set('popular_movies', content, timeout = CACHE_TTL)
        return json2obj(json.dumps(content))

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class MovieRentalType(DjangoObjectType):
    class Meta:
        model = models.MovieRental
        interfaces = (graphene.Node, )

class MovieDetailType(graphene.ObjectType):
    vote_count = graphene.Int()
    id = graphene.ID()
    video = graphene.Boolean()
    vote_average = graphene.Float()
    title = graphene.String()
    popularity = graphene.Float()
    poster_path = graphene.String()
    original_language = graphene.String()
    original_title = graphene.String()
    backdrop_path = graphene.String()
    adult = graphene.Boolean()
    overview = graphene.String()
    release_date = graphene.String()

class MovieReviewType(graphene.ObjectType):
    id = graphene.ID()
    author = graphene.String()
    content = graphene.String()
    url = graphene.String()

class Query(graphene.ObjectType):
    all_rentals = graphene.List(MovieRentalType)

    def resolve_all_rentals(self, info, **args):
        return models.MovieRental.objects.all()

    rental = graphene.Field(MovieRentalType, id=graphene.ID())

    def resolve_rental(self, info, **args):
        rid = from_global_id(args.get('id'))
        return models.MovieRental.objects.get(pk=rid[1])

    my_rentals = graphene.List(MovieRentalType, id=graphene.ID())

    def resolve_my_rentals(self, info, **args):
        context = info.context
        if context.user.is_authenticated:
            return models.MovieRental.objects.filter(user = context.user)

    popular_movies = graphene.List(MovieDetailType)

    def resolve_popular_movies(self, info, **args):
        return get_popular_movies()

    # movie_review = graphene.List(MovieReviewType, id=graphene.Int())
    movie_review = graphene.List(MovieReviewType, id=graphene.Int())

    def resolve_movie_review(self, info, **args):
        movie_id = args.get('id')
        reviews = requests.get('https://api.themoviedb.org/3/movie/'+ str(movie_id) +'/reviews?api_key=8879bf0d7d0370ed12d9245c5c774ae1&language=en-US&page=1')
        content = json.loads(reviews.content)['results']
        return json2obj(json.dumps(content))

    movie_query_by_title = graphene.List(MovieDetailType, query=graphene.String())

    def resolve_movie_query_by_title(self, info, **args):
        query = args.get('query')
        query_results = requests.get('https://api.themoviedb.org/3/search/movie?api_key=8879bf0d7d0370ed12d9245c5c774ae1&language=en-US&query=' + query + '&page=1&include_adult=false')
        content = json.loads(query_results.content)['results']
        return json2obj(json.dumps(content))

    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    me = graphene.Field(UserType)

    def resolve_me(self, info, **kwargs):
        return info.context.user

class CreateRentalMutation(graphene.Mutation):
    class Arguments:
        movieId = graphene.Int(required=True)

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MovieRentalType)

    @staticmethod
    def mutate(self, info, movieId):
        context = info.context
        if not context.user.is_authenticated:
            return CreateRentalMutation(status=403)
        if not movieId: #do some validation here
            return CreateRentalMutation(
                status=400,
                formErrors = json.dumps(
                    {'message' : ['No movie selected']}
                ))
        obj = models.MovieRental.objects.create(
            user = context.user, movieId = movieId
        )
        return CreateRentalMutation(status=200, message=obj)

class ReturnRentalMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MovieRentalType)

    @staticmethod
    def mutate(self, info, id):
        context = info.context
        if not context.user.is_authenticated:
            return ReturnRentalMutation(status=403)
        if not id:
            return CreateRentalMutation(
                status=400,
                formErrors = json.dumps(
                    {'message' : ['No movie selected to return']}
                ))
        obj = models.MovieRental.objects.get(id = id)
        obj.returnDate = datetime.now()
        obj.save(['returnDate'])
        return ReturnRentalMutation(status=200, message=obj)

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_rental = CreateRentalMutation.Field()

