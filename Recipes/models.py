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
            action.save()

            i = i - 1

        action.instruction_number = position


class GeneralAction(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='actions')

    choices = (
        ('RT', 'Basic Return Text'),
        )

    instruction_number = models.IntegerField()
    type = models.CharField(max_length=2, choices=choices)

    return_statement = models.TextField()

    def basic_return_text(self):
        next_instruction = self.instruction_number + 1
        return_statement = self.return_statement

        return (next_instruction, return_statement)

    def get_action(self):
        if self.choice == 'RT':
            return self.basic_return_text()


class AppSession(models.Model):
    last_modified = models.DateTimeField(auto_now=True)
    program_counter = models.IntegerField()
    user = models.ForeignKey('accounts.User')
    current_app = models.ForeignKey(Recipe)
    end = models.BooleanField(default=False)

    def next_action(self):
        action = self.current_app.actions.get(
            instruction_number=self.program_counter)
        (next_instruction, return_statement) = action.get_action()
        self.program_counter = next_instruction
        self.save()

        return return_statement
