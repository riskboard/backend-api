from django.contrib import admin
from .models.actor.actor import Actor

# Register your models here.
admin.site.register([
  Actor,
])