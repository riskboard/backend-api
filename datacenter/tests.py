from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import DataCenter
from .serializers import DataCenterSerializer

# Create your tests here.
class BaseViewTest(APITestCase):
  client = APIClient()

  @staticmethod
  def create_datacenter():
    if title != '' and artist != '':
      DataCenter.objects.create(title=title, artist=artist)

  def setup(self):
    # add test data
    self.