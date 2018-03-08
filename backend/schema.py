import graphene
import rental.schema

class Queries(
    rental.schema.Query,
    graphene.ObjectType,
):
    pass

class Mutations(
    rental.schema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Queries, mutation=Mutations)