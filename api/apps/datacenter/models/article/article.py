from djongo import models

from ..actor.actor import Actor
from .gkg_theme import GKGTheme
from .keyword import Keyword

class Article(models.Model):
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article
  '''
  url = models.TextField(max_length=300)
  date = models.DateField(db_index=True)
  language = models.TextField(max_length=30)

  keywords = models.ArrayReferenceField(Keyword)
  gkg_themes = models.ArrayReferenceField(GKGTheme)
  actors = models.ArrayReferenceField(Actor)