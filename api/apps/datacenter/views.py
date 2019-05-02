from rest_framework import generics
from rest_framework.views import APIView
from .models.actor.actor import Actor
from .serializers.actor.actorserializer import ActorSerializer
from .processors.gkg_processor import GKGProcessor
from .query.query import Query

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
      start_date = request.data['start_date'] if 'start_date' in request.data else None
      end_date = request.data['end_date'] if 'end_date' in request.data else None
      locations = request.data['locations'].split(',') if 'locations' in request.data else None
      keywords = request.data['keywords'].split(',') if 'keywords' in request.data else None
      gkg_themes = request.data['gkg_themes'].split(',') if 'gkg_themes' in request.data else None
      query = Query(start_date=start_date, end_date=end_date, gkg_themes=gkg_themes, keywords=keywords, locations=locations)
      GKGProcessor(query)