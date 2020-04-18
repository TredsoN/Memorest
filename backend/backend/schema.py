import graphene

from graphql_auth.schema import UserQuery, MeQuery

from user.schema import AuthMutation
from memory.schema import MemoryMutation, MemoryQuery


class Query(UserQuery, MeQuery, MemoryQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, MemoryMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
