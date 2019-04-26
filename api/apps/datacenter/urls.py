from django.urls import path
from .views import ListActorView

urlpatterns = [
  path('datacenter/', ListActorView.as_view(), name='actor-all')
]