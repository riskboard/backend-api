from rest_framework import generics
from rest_framework.views import APIView
from .models.actor.actor import Actor
from .serializers.actor.actorserializer import ActorSerializer
from .processors.gkg_processor import GKGProcessor

class ListActorView(generics.ListAPIView):
  '''
  Provides a get method handler
  '''
  queryset = Actor.objects.all()
  serializer_class = ActorSerializer

class DataCenterView(APIView):
  '''
  Parses articles from a given date.
  '''

  def post(self, request, *args, **kwargs):
    if self.request.version == 'v1':
      start_date = request.data['start_date']
      end_date = request.data['end_date']
      GKGProcessor(start_date, end_date)