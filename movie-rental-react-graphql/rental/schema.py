import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
import json
import requests
from collections import namedtuple

from . import models


def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

class MovieRentalType(DjangoObjectType):
    class Meta:
        model = models.MovieRental
        interfaces = (graphene.Node, )

class PopularMovieType(graphene.ObjectType):
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

class Query(graphene.ObjectType):
    all_rentals = graphene.List(MovieRentalType)

    def resolve_all_rentals(self, info, **args):
        return models.MovieRental.objects.all()

    rental = graphene.Field(MovieRentalType, id=graphene.ID())

    def resolve_rental(self, info, **args):
        rid = from_global_id(args.get('id'))
        return models.MovieRental.objects.get(pk=rid[1])

    popular_movies = graphene.List(PopularMovieType)

    def resolve_popular_movies(self, info, **args):
        print("this is called")
        popular = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=8879bf0d7d0370ed12d9245c5c774ae1&language=en-US&page=1')
        content = json.loads(popular.content)["results"]
        jsonout = json2obj(json.dumps(content))
        return jsonout


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
                    {'message' : ['Please enter a movieId']}
                ))
        obj = models.MovieRental.objects.create(
            user = context.user, movieId = movieId
        )
        return CreateRentalMutation(status=200, message=obj)


class Mutation(graphene.ObjectType):
    create_rental = CreateRentalMutation.Field()

