from __future__ import unicode_literals

from django.db import models


class AppSession(models.Model):
    user = models.ForeignKey('accounts.User')
    amazon_echo = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(auto_now=True)
    program_counter = models.IntegerField(default=1)
    current_app = models.ForeignKey('Recipes.Recipe')
    end = models.BooleanField(default=False)

    def next_action(self):
        length = self.current_app.actions.count()
        if length < self.program_counter:
            self.end = True
            self.save()
            return 'You have reached the end of this application'

        action = self.current_app.actions.get(
            instruction_number=self.program_counter)
        (next_instruction, return_statement) = action.get_action()
        self.program_counter = next_instruction
        self.save()

        return return_statement
