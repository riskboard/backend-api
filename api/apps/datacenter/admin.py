from django.contrib import admin
from .models.actor.actor import Actor
from .models.article.article import Article

# Register your models here.
admin.site.register([
  Actor,
  Article,
])