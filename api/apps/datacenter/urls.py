from django.urls import path
from .views import ListActorView, DataCenterView

urlpatterns = [
  path('datacenter/actors/', ListActorView.as_view(), name='actor-all'),
  path('datacenter/', DataCenterView.as_view(), name='datacenter')
]