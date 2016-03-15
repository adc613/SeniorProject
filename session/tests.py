from django.test import TestCase

from Recipes.models import Recipe, GeneralAction, BasicReturnText
from accounts.models import User, LinkAccountToEcho
from .models import AppSession


class ResponseTestCases(TestCase):

    def setUp(self):
        self.password = '$tr0ngPa$$w0rd'
        self.user = User.objects.create_user(
            first_name='Adam',
            last_name='Collins',
            email='adc82@case.edu',
            password=self.password
            )

        self.recipe = Recipe.objects.create(
            creator=self.user,
            name='First App',
            description='First Description'
            )

        self.basic_return_text = BasicReturnText.objects.create(
            return_statement='Hello World!'
            )
        self.general_action = GeneralAction.objects.create(
            type='RT',
            basic_return_text=self.basic_return_text
            )

        basic_return_text2 = BasicReturnText.objects.create(
            return_statement='Hello World!2'
            )
        general_action2 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text2
            )

        basic_return_text3 = BasicReturnText.objects.create(
            return_statement='Hello World!3'
            )
        general_action3 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text3
            )

        basic_return_text4 = BasicReturnText.objects.create(
            return_statement='Hello World!4'
            )
        general_action4 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text4
            )

        basic_return_text5 = BasicReturnText.objects.create(
            return_statement='Hello World!5'
            )
        general_action5 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text5
            )
        self.recipe.insert_action(self.general_action, 0)
        self.recipe.insert_action(general_action2, 0)
        self.recipe.insert_action(general_action3, 0)
        self.recipe.insert_action(general_action4, 0)
        self.recipe.insert_action(general_action5, 0)

        self.actions = [self.general_action, general_action2, general_action3,
                        general_action4, general_action5]

    def test_app_session_model_next_action(self):
        session = AppSession.objects.create(
            user=self.user,
            amazon_echo='1lkjh342k41j4kl1j34',
            current_app=self.recipe
            )

        for action in self.actions:
            return_statement = session.next_action()
            self.assertEqual(return_statement, action.get_action()[1])

    def test_registering_echo(self):
        link = LinkAccountToEcho.objects.create(user=self.user)
        if link:
            return 1

    def test_session_has_not_started(self):
        pass

    def test_echo_is_in_session(self):
        pass

    def test_echo_sessions_has_ended(self):
        pass
