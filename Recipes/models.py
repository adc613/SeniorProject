from __future__ import unicode_literals

from django.db import models


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


class BasicReturnText(models.Model):
    return_statement = models.TextField()

    def action(self, instruction_number):
        next_instruction = instruction_number + 1
        return_statement = self.return_statement

        return (next_instruction, return_statement)


class GeneralAction(models.Model):
    recipe = models.ForeignKey(Recipe, null=True, related_name='actions')

    choices = (
        ('RT', 'Basic Return Text'),
        )

    instruction_number = models.IntegerField(default=-1)
    type = models.CharField(max_length=2, choices=choices)

    basic_return_text = models.OneToOneField(BasicReturnText, null=True)

    def get_action(self):
        if self.type == 'RT':
            action = self.basic_return_text
        instruction = self.instruction_number
        return action.action(instruction)
