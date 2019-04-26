import urllib
import logging
from djongo import models

from bs4 import BeautifulSoup
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from pycountry import languages
from langdetect import detect
from rake_nltk import Rake

from ..actor.actor import Actor

class Article(models.Model):
  '''
  Defines the Article class. An article refers to
  a specific article, for example a Twitter article,
  a news article
  '''
  SENTENCE_COUNT = 4
  url = models.TextField(max_length=300)
  actors = models.ManyToManyField(Actor)

  @property
  def text_params(self):
    text = extractText(url)
    language = languages.get(alpha_2=detect(text)).name
    parser = HtmlParser.from_url(url, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    summary = ''
    for sentence in summarizer(parser.document, Article._SENTENCE_COUNT):
      summary += str(sentence)

    r = Rake(language, max_length=3)
    r.extract_keywords_from_text(text)
    keywords = r.get_ranked_phrases()[:10]

    return language, keywords, summary

  def extractText(url):
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

  def save(self, *args, **kwargs):
    self.language, self.keywords, self.summary = self.text_params()
    super(Article, self).save(*args, **kwargs)