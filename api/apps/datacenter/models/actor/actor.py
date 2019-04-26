from djongo import models

from metaphone import doublemetaphone

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
    max_length=50
  )

  actor_name = models.CharField(
    max_length=200
  )

  @property
  def metaphone_name(self):
    metaphone_name = doublemetaphone(self.actor_name)
    return (metaphone_name[0] + metaphone_name[1])

  def save(self, *args, **kwargs):
    self.metaphone_name = self.metaphone_name()
    super(Actor, self).save(*args, **kwargs)