from __future__ import unicode_literals

from django.db import models

import requests


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('accounts.User')
    description = models.TextField()

    def insert_action(self, action, position):
        if action.recipe != self and action.recipe is not None:
            return None
        from Recipes.models import GeneralAction
        if position <= 0:
            position = self.actions.count() + 1

        number_of_actions = self.actions.count()

        if position < 0 or position > number_of_actions:
            position = number_of_actions + 1

        i = number_of_actions
        while i >= position:
            temp_action = GeneralAction.objects.get(recipe=self,
                                                    instruction_number=i)
            temp_action.instruction_number = temp_action.instruction_number + 1
            temp_action.save()

            i = i - 1

        action.instruction_number = position
        action.recipe = self
        action.save()

        return action

    def add_action(self, action):
        return self.insert_action(action, -1)


class APICall(models.Model):
    get_or_post_choice = (
        ('G', 'get'),
        ('P', 'post'),
        )

    url = models.CharField(max_length=2048)
    is_get = models.BooleanField(default=True)
    json_string = models.TextField()

    def action(self):
        try:
            if self.is_get:
                requests.get(self.url, data=self.json_string)
            else:
                requests.post(self.url, data=self.json_string)
            return True
        except:
            return False


class BasicReturnText(models.Model):
    return_statement = models.TextField()

    def action(self, instruction_number):
        next_instruction = instruction_number + 1
        return_statement = self.return_statement

        return (next_instruction, return_statement)


class GeneralAction(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, related_name='actions')

    choices = (
        ('NS', 'Not Specified'),
        ('RT', 'Basic Return Text'),
        )

    instruction_number = models.IntegerField(default=-1)
    type = models.CharField(max_length=2, choices=choices, default='RT')
    is_api_call = models.BooleanField(default=False)

    basic_return_text = models.OneToOneField(BasicReturnText,
                                             null=True,
                                             related_name='general_action')
    api_call = models.OneToOneField(APICall,
                                    null=True,
                                    related_name='general_action')

    def get_action(self):
        if self.is_api_call:
            self.api_call.action()
        if self.type == 'RT':
            action = self.basic_return_text
        instruction = self.instruction_number

        return action.action(instruction)
