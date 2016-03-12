from __future__ import unicode_literals

from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('accounts.User')
    description = models.TextField()

    def insert_action(self, action, position):
        from Recipes.models import GeneralAction
        if position < 0:
            position = self.actions.count() + 1

        number_of_actions = self.actions.count()
        i = number_of_actions

        if position < 0 or position > number_of_actions:
            position = number_of_actions + 1

        while i >= position:
            action = GeneralAction.objects.get(recipe=self,
                                               instruction_number=i)
            action.instruction_number = action.instruction_number + 1

            i = i - 1

        action.instruction_number = position

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
    recipe = models.ForeignKey(Recipe, related_name='actions')

    choices = (
        ('RT', 'Basic Return Text'),
        )

    instruction_number = models.IntegerField(unique=True)
    type = models.CharField(max_length=2, choices=choices)

    basic_return_text = models.OneToOneField(BasicReturnText, null=True)

    def get_action(self):
        if self.choice == 'RT':
            action = self.basic_return_text
        instruction = self.instruction_number
        next_instruction, return_statement = action.action(instruction)
        self.instruction_number = next_instruction

        return return_statement
