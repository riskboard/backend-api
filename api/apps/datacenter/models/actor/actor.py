from djongo import models

class Actor(models.Model):
  '''
  Defines the Actor class, which can represent
  an organization, a person, or a notable group

  TODO: Add actor location
  '''
  ORGANIZATION = 'ORG'
  PERSON = 'PER'
  ACTOR_TYPE_CHOICES = (
    (ORGANIZATION, 'Organization'),
    (PERSON, 'Person')
  )

  actor_type = models.CharField(
    choices=ACTOR_TYPE_CHOICES,
    default=ORGANIZATION,
    null=False,
    max_length=50,
    db_index=True
  )

  actor_name = models.CharField(
    max_length=200
  )

  metaphone_name = models.CharField(
    max_length=100,
    db_index=True
  )