import logging
from metaphone import doublemetaphone

from ..models.actor.actor import Actor
from ..models.article.article import Article

# from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'Organization'
TYPE_PERSON = 'Person'

def extract_and_filter_data(data, query):
  '''
  Extracts the url, people, organizations, and location from
  one row in the GKG dataframe
  '''
  people_names = extract_data_list('Persons', data)
  org_names = extract_data_list('Organizations', data)

  actor_names = people_names+org_names
  if not len(actor_names):
    return False

  # locations = extractLocations(data)

  gkg_themes = set(extract_data_list('Themes', data))

  if query and not query.filter_article(actor_names, gkg_themes): return False

  # locationIDs = [loc.storeDB(db) for loc in locations]

  people = [find_or_create_actor(actor_type=TYPE_PERSON, actor_name=name) for name in people_names]

  orgs = [find_or_create_actor(actor_type=TYPE_ORGANIZATION, actor_name=name) for name in org_names]

  actors = people+orgs

  url = str(data['DocumentIdentifier'])
  article = Article.objects.create(url=url, actors=actors)

  return article, actors

def find_or_create_actor(actor_type, actor_name):
  # find an actor with the existing name
  metaphone_name = doublemetaphone(actor_name)
  matched_name = metaphone_name[0] + metaphone_name[1]

  existing_actor = Actor.objects.filter(metaphone_name=matched_name)
  if not len(existing_actor):
    return Actor.objects.create(actor_type=TYPE_PERSON, actor_name=name)
  return existing_actor[0]

def extract_data_list(field_name, data):
  '''
  extracts list from fieldNames
  '''
  return list(filter(lambda x: x!= 'nan', str(data[field_name]).split(';')))