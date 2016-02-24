from __future__ import unicode_literals

from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length = 200)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    description = models.TextField()
    FirstAction = models.ForeignKey('Recipes.GeneralAction', null=True)

class GeneralAction(models.Model):
    ReturnStatement = models.TextField()
    NextAction = models.ForeignKey('Recipes.GeneralAction', null=True)
    





