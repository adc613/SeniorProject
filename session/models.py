from __future__ import unicode_literals

from django.db import models

from Recipes.models import ConditionalHeader


class AppSession(models.Model):
    user = models.ForeignKey('accounts.User')
    amazon_echo = models.CharField(max_length=255, unique=True)
    last_modified = models.DateTimeField(auto_now=True)
    program_counter = models.IntegerField(default=1)
    current_app = models.ForeignKey('Recipes.Recipe')
    end = models.BooleanField(default=False)

    is_entering_conditional = models.BooleanField(default=False)
    is_in_conditional = models.BooleanField(default=False)
    conditional_session = models.OneToOneField('session.ConditionalSession',
                                               null=True,
                                               related_name='parent_session')

    def get_current_branch(self):
        return self.current_app

    def enter_conditional_branch(self, branch):
        from session.models import ConditionalSession
        self.conditional_session = ConditionalSession.objects.create(
            user=self.user,
            amazon_echo=self.amazon_echo,
            current_branch=branch
            )
        (next_instruction, return_statement) = \
            self.conditional_session.next_action()
        self.is_entering_conditional = False
        self.is_in_conditional = True
        self.save()

        return (next_instruction, return_statement)

    def next_action(self, **kwargs):
        current_app = self.get_current_branch()
        if not self.is_in_conditional:
            # Regularrly iterate through actions
            length = current_app.actions.count()
            if length < self.program_counter:
                self.end = True
                self.save()

                return 'You have reached the end of this application'

            action = current_app.actions.get(
                instruction_number=self.program_counter)
            (next_instruction, return_statement) = action.get_action()
            if next_instruction >= 0:
                # next_instruction >= 0 means that we are not in a conditional
                self.program_counter = next_instruction
                self.save()

                return return_statement

            elif next_instruction == -1:
                # next_instruciton == -1 means we're entering a conditional
                self.is_entering_conditional = True

                return return_statement

        elif self.is_entering_conditional:
            action = current_app.actions.get(
                instruction_number=self.program_counter)
            (status, branch) = \
                action.get_action(branch_number=kwargs['branch_number'])

            return self.enter_conditional_branch(branch)

        else:
            (next_instruction, return_statement) = \
                self.conditional_session.next_action()
            if self.conditional_session.end:
                self.is_in_conditional = False
                self.program_counter = self.program_counter + 1
                self.save()

            return return_statement


class ConditionalSession(AppSession):
    current_branch = models.ForeignKey(ConditionalHeader)

    def get_current_branch(self):
        return self.current_branch
