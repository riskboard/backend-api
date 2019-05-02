from djongo import models

class GKGTheme(models.Model):
  '''
  Defines the GKG Theme model.
  '''
  theme = models.TextField(unique=True, max_length=100)