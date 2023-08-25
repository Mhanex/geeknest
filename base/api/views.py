from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from base.api import serializers
from . serializers import GroupSerializer


@api_view(['GET'])
def getRoutes(request):
     # Define a list of available routes along with their HTTP methods and endpoints
    routes = [
        'GET /api',
        'GET /api/groups',
        'GET /api/groups/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def getGroups(request):
    groups = Room.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getGroup(request, pk):
    group = Room.objects.get(id=pk)
    serializer = GroupSerializer(group, many=False)
    return Response(serializer.data)

