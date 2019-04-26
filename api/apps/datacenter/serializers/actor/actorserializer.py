from rest_framework import serializers
from ...models.actor.actor import Actor

class ActorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Actor
    fields = ('actor_name', 'actor_type')