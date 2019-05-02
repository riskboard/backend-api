from ..models.article.gkg_theme import GKGTheme

class Query():
  '''
  Defines a Query class. A Query can include themes, keywords, languages, coordinates, and locations
  '''
  def __init__(self, start_date, end_date, gkg_themes=None, keywords=None,
  languages=None, locations=None):
    self.start_date = start_date
    self.end_date = end_date
    self.gkg_themes = set(gkg_themes) if gkg_themes else None
    self.keywords = set(keywords) if keywords else None
    self.languages = set(languages) if languages else None
    self.locations = set(locations) if locations else None

  def filter_article(self, article_themes=None, article_kwds=None,
  article_language=None, article_coordinates=None, article_locations=None):
    '''
    Filters based on the established Query
    '''
    if self.gkg_themes and not self.filter_themes(article_themes):
      return False
    if self.keywords and not self.filter_keywords(article_kwds):
      return False
    if self.languages and not self.filter_language(article_language):
      return False
    if self.locations and not self.filter_location(article_locations):
      return False
    return True

  def filter_themes(self, article_themes):
    if not article_themes: return False
    return (self.gkg_themes & set(article_themes))

  def filter_keywords(self, article_kwds):
    if not article_kwds: return False
    return (self.keywords & set(article_kwds))

  def filter_language(self, article_language):
    return article_language in self.languages

  def filter_location(self, article_locations):
    return (self.locations & set(article_locations))