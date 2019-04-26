from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models.actor.actor import Actor
from .serializers.actor.actorserializer import ActorSerializer

# Create your tests here.
class BaseViewTest(APITestCase):
  client = APIClient()

  @staticmethod
  def create_actor(actor_name='', actor_type=''):
    if actor_name != '' and actor_type != '':
      Actor.objects.create(actor_name=actor_name, actor_type=actor_type)

  def set_up(self):
    # add test actors
    self.create_actor('Barack Obama', 'Person')
    self.create_actor('Robert Downing', 'Person')
    self.create_actor('Greenpeace', 'Organization')

class GetAllActorsTest(BaseViewTest):
  def test_get_all_actors(self):
    '''
    This test ensures that all actors in the set_up method exist when we make a GET request to the datacenter/ endpoint
    '''
    # hit the API Endpoint
    response = self.client.get(
      reverse('actor-all', kwargs={'version': 'v1'})
    )

    # fetch the data from the database
    expected = Actor.objects.all()
    serialized = ActorSerializer(expected, many=True)
    self.assertEqual(response.data, serialized.data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)