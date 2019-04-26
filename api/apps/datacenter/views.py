from rest_framework import generics
from .models.actor.actor import Actor
from .serializers.actor.actorserializer import ActorSerializer

# Create your views here.
class ListActorView(generics.ListAPIView):
  '''
  Provides a get method handler
  '''
  queryset = Actor.objects.all()
  serializer_class = ActorSerializer