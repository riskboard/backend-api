from rest_framework import serializers
from ...models.article.article import Article

class ActorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Article
    fields = ('url', 'actors')