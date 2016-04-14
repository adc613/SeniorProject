from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# import requests

import json
import subprocess


@python_2_unicode_compatible
class Recipe(models.Model):
    is_conditional_branch = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('accounts.User', null=True)
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    parent_header = models.ForeignKey('Recipes.ConditionalHeader',
                                      related_name='branches',
                                      null=True)
    branch_number = models.IntegerField(default=-1)

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

    def __str__(self):
        if self.is_conditional_branch:
            return 'Branch {}'.format(self.branch_number)
        else:
            return 'App {}'.format(self.name)

    def get_user(self):
        if self.is_conditional_branch:
            return self.parent_header.get_user()
        else:
            return self.creator


class ConditionalHeader(models.Model):
    question = models.TextField()

    def get_branches(self):
        return self.branches.all()

    def get_branch(self, branch_number):
        return Recipe.objects.get(parent_header=self,
                                  branch_number=branch_number)

    def add_branch(self, branch):
        branch.branch_number = self.branches.count()
        branch.save()

    def get_user(self):
        return self.general_action.get_user()


class APICall(models.Model):
    url = models.CharField(max_length=2048)
    is_get = models.BooleanField(default=True)
    json_string = models.TextField()

    def action(self):
        try:
            data = json.loads(self.json_string)
            bashCommand = "curl {} -d \"args={}\"".format(self.url,
                                                          data['args'])
            subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            """
            if self.is_get:
                requests.get(self.url, params=json.loads(self.json_string))
            else:
                requests.post(self.url, params=json.loads(self.json_string))
            """
            return True
        except:
            return False


class BasicReturnText(models.Model):
    return_statement = models.TextField()

    def action(self, instruction_number):
        next_instruction = instruction_number + 1
        return (next_instruction, self.return_statement)


class GeneralAction(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, related_name='actions')
    NOT_SPECIFIED = 'NS'
    BASIC_RETURN_TEXT = 'RT'
    CONDITIONAL = 'C'

    choices = (
        (NOT_SPECIFIED, 'Not Specified'),
        (BASIC_RETURN_TEXT, 'Basic Return Text'),
        (CONDITIONAL, 'Conditional'),
        )

    instruction_number = models.IntegerField(default=-1)
    type = models.CharField(max_length=2, choices=choices, default='RT')
    is_api_call = models.BooleanField(default=False)

    # Actions
    basic_return_text = models.OneToOneField(BasicReturnText,
                                             null=True,
                                             related_name='general_action')
    api_call = models.OneToOneField(APICall,
                                    null=True,
                                    related_name='general_action')
    conditional = models.OneToOneField(ConditionalHeader,
                                       null=True,
                                       related_name='general_action')

    def get_action(self, **kwargs):
        if self.is_api_call:
            self.api_call.action()
        if self.type == self.CONDITIONAL:
            return (-1, self.conditional.get_branch(kwargs['branch_number']))
        elif self.type == self.BASIC_RETURN_TEXT:
            action = self.basic_return_text
        instruction = self.instruction_number

        return action.action(instruction)

    def get_question(self):
        return self.conditional.question

    def __str__(self):
        return "Type:{} App:{} Instruction Number:{} ".format(
            self.type, self.recipe, self.instruction_number)

    def get_user(self):
        return self.recipe.get_user()
