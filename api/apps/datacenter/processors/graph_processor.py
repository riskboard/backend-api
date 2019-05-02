import logging
import urllib
from metaphone import doublemetaphone
from bs4 import BeautifulSoup
from pycountry import languages
from langdetect import detect
from rake_nltk import Rake

from ..models.actor.actor import Actor
from ..models.article.article import Article
from ..models.article.gkg_theme import GKGTheme
from ..models.article.keyword import Keyword

from ..utils.utils import metaphone_name

# from DataCenter.Geo.GDeltLocation import GDeltLocation

TYPE_ORGANIZATION = 'Organization'
TYPE_PERSON = 'Person'

def extract_and_filter_data(data, query, date):
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

  gkg_themes = extract_gkg_themes(data)

  if query and not query.filter_article(actor_names, gkg_themes): return False

  # locationIDs = [loc.storeDB(db) for loc in locations]

  people = [find_or_create_actor(actor_type=TYPE_PERSON, actor_name=name) for name in people_names]

  orgs = [find_or_create_actor(actor_type=TYPE_ORGANIZATION, actor_name=name) for name in org_names]

  actors = people+orgs

  url = str(data['DocumentIdentifier'])
  language, kwds = get_article_params(url)

  article = Article.objects.create(url=url, date=date, language=language)

  article.actors.add(*actors)
  article.keywords.add(*kwds)
  article.gkg_themes.add(*gkg_themes)

  return article, actors

def extract_gkg_themes(data):
  theme_strs = extract_data_list('Themes', data)
  themes = []
  for theme_str in theme_strs:
    query = GKGTheme.objects.filter(theme=theme_str)
    if not len(query):
      themes.append(GKGTheme.objects.create(theme=theme_str))
    else: themes.append(query[0])
  return themes

def find_or_create_actor(actor_type, actor_name):
  # find an actor with the existing name
  met_name = metaphone_name(actor_name)

  existing_actor = Actor.objects.filter(metaphone_name=met_name)

  if not len(existing_actor):
    return Actor.objects.create(
      actor_type=actor_type,
      actor_name=actor_name,
      metaphone_name=met_name)
  return existing_actor[0]

def extract_data_list(field_name, data):
  '''
  extracts list from fieldNames
  '''
  return list(filter(lambda x: x!= 'nan', str(data[field_name]).split(';')))

def get_article_params(url):
  SENTENCE_COUNT=4
  text = extractText(url)
  language = languages.get(alpha_2=detect(text)).name

  r = Rake(language, max_length=3)
  r.extract_keywords_from_text(text)

  kwd_strings = r.get_ranked_phrases()[:10]
  kwds = []
  for kwd_str in kwd_strings:
    query = Keyword.objects.filter(keyword=kwd_str)
    if not len(query):
      kwds.append(Keyword.objects.create(keyword=kwd_str))
    else: kwds.append(query[0])

  return language, kwds

def extractText(url):
  try:
    with urllib.request.urlopen(url) as url:
      html = url.read()

    soup = BeautifulSoup(html, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    # get text
    text = soup.body.get_text(separator=' ')
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text
  except:
    return ''