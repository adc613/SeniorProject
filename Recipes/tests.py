from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from accounts.models import User
from .models import Recipe, GeneralAction


class RecipesViewsTestCases(TestCase):

    def setUp(self):
        self.password = '$tr0ngPa$$w0rd'
        self.user = User.objects.create_user(
            first_name='Adam',
            last_name='Collins',
            email='adc82@case.edu',
            password=self.password
            )

    def test_create_recipe(self):
        c = Client()

        resp = c.get(reverse('Recipes:create_recipe'))
        self.assertEqual(resp.status_code, 302)

        c.login(username=self.user.email, password=self.password)
        resp = c.get(reverse('Recipes:create_recipe'))
        self.assertEqual(resp.status_code, 200)

        description = 'This is my first application'
        name = 'My First App'
        resp = c.post(reverse('Recipes:create_recipe'), {
                      'description': description,
                      'name': name
                      })
        self.assertEqual(resp.status_code, 302)
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.creator, self.user)
        self.assertEqual(recipe.description, description)
        self.assertEqual(recipe.name, name)

    def test_add_actions_to_recipe(self):
        description = 'This is my first application'
        name = 'My First App'
        recipe = Recipe.objects.create(
            creator=self.user,
            name=name,
            description=description
            )
        c = Client()

        resp = c.get(reverse('Recipes:create_action', kwargs={'recipe_pk': 1}))
        self.assertEqual(resp.status_code, 302)

        c.login(username=self.user.email, password=self.password)
        resp = c.get(reverse('Recipes:create_action', kwargs={'recipe_pk': 1}))
        self.assertEqual(resp.status_code, 200)

        return_statement = 'Hello Welcome to Echo'
        resp = c.post(reverse('Recipes:create_action',
                              kwargs={'recipe_pk': 1}),
                      {'type': 'RT',
                       'return_statement': return_statement})

        self.assertEqual(resp.status_code, 302)

        action = GeneralAction.objects.get(pk=1)
        self.assertEqual(action.recipe, recipe)
        self.assertEqual(action.type, 'RT')
        self.assertEqual(action.instruction_number, 1)
        self.assertEqual(action.basic_return_text.return_statement,
                         return_statement)


class RecipesModelsTestCases(TestCase):

    def setUp(self):
        pass

    def test_recipe_insert_action(self):
        pass

    def test_recipe_add_action(self):
        pass

    def test_basic_return_text_action(self):
        pass

    def test_general_action_get_action(self):
        pass
