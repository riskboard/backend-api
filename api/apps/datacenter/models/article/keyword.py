from djongo import models

class Keyword(models.Model):
  '''
  Defines the GKG Theme model.
  '''
  keyword = models.TextField(unique=True, max_length=100)