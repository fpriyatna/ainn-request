import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from models import Request as RequestModel
from models import Response as ResponseModel


class Request(MongoengineObjectType):
    class Meta:
        model = RequestModel
        interfaces = (Node, )


class Response(MongoengineObjectType):
    class Meta:
        model = ResponseModel
        interfaces = (Node,)


class CreateRequest(graphene.Mutation):

    class Arguments:
        requester_id = graphene.String()
        dataset_id = graphene.String()
        description = graphene.String()

    request = graphene.Field(Request)

    def mutate(self, info, **kwargs):
        request = RequestModel(**kwargs)
        request.save()
        return CreateRequest(request=request)


class Query(graphene.ObjectType):
    node = Node.Field()
    # all_requests = MongoengineConnectionField(Request)
    # all_responses = MongoengineConnectionField(Response)
    request = MongoengineConnectionField(Request)
    #request = graphene.Field(Request)
    response = MongoengineConnectionField(Response)
    # hello = graphene.String(description='A typical hello world')
    #
    # def resolve_hello(self, info):
    #     return 'World'


class Mutation(graphene.ObjectType):
    create_request = CreateRequest.Field()


schema = graphene.Schema(query=Query, types=[Request, Response], mutation=Mutation)
