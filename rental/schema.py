import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
import json

from . import models

class MovieRentalType(DjangoObjectType):
    class Meta:
        model = models.MovieRental
        interfaces = (graphene.Node, )

class Query(graphene.AbstractType):
    all_rentals = graphene.List(MovieRentalType)

    def resolve_all_rentals(self, info, **args):
        return models.MovieRental.objects.all()

    rental = graphene.Field(MovieRentalType, id=graphene.ID())

    def resolve_rental(self, info, **args):
        rid = from_global_id(args.get('id'))
        return models.MovieRental.objects.get(pk=rid[1])

class CreateRentalMutation(graphene.Mutation):
    class Input:
        movieId = graphene.Int()

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MovieRentalType)

    @staticmethod
    def mutate(root, args, context, info):
        if not context.user.is_auth():
            return CreateRentalMutation(status=403)
        movieId = args.get('movieId')
        if not movieId:
            return CreateRentalMutation(status=400,
            formErrors= json.dumps(
                {'message' : ['Please enter a movieId']}
            ))
            obj = models.MovieRental.objects.create(
                user = context.user, movieId = movieId
            )
            return CreateRentalMutation(status=200, message=obj)


class Mutation(graphene.AbstractType):
    create_rental = CreateRentalMutation.Field()

