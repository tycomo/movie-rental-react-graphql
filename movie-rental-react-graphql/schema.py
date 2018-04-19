import graphene
import graphql_jwt
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
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Queries, mutation=Mutations)