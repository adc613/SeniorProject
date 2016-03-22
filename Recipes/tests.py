from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from accounts.models import User
from .models import Recipe, GeneralAction, BasicReturnText, APICall

import json


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

    def test_add_api_call(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)
        recipe = Recipe.objects.create(
            creator=self.user,
            name='First App',
            description='First Description'
            )

        basic_return_text = BasicReturnText.objects.create(
            return_statement='Hello World!'
            )

        general_action = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text
            )
        general_action.recipe = recipe
        general_action.save()

        pk = general_action.pk
        resp = c.get(reverse('Recipes:add_api_call', kwargs={'pk': pk}))
        self.assertEqual(resp.status_code, 200)

        json_string = {'title': 'foo', 'body': 'bar', 'userId': 1}

        data = {'url': 'http://jsonplaceholder.typicode.com/posts/1',
                'is_get': True,
                'json_string': json.dumps(json_string)
                }
        resp = c.post(reverse('Recipes:add_api_call', kwargs={'pk': pk}),
                      data)
        api_call = APICall.objects.get(pk=1)
        action = GeneralAction.objects.get(pk=pk)
        self.assertEqual(api_call, action.api_call)
        self.assertEqual(api_call.url, data['url'])
        self.assertEqual(api_call.json_string, data['json_string'])
        self.assertEqual(api_call.is_get, data['is_get'])
        self.assertEqual(resp.status_code, 302)
        api_call.action()

        data = {'url': 'http://jsonplaceholder.typicode.com/posts',
                'is_get': False,
                'json_string': json.dumps(json_string)
                }
        resp = c.post(reverse('Recipes:add_api_call', kwargs={'pk': pk}),
                      data)
        print('-------hello-----')
        print(api_call.url)
        api_call = APICall.objects.get(pk=2)
        print(api_call.url)
        print(api_call.is_get)
        print('-------goodbye-----')
        action = GeneralAction.objects.get(pk=pk)
        self.assertEqual(api_call, action.api_call)
        self.assertEqual(api_call.url, data['url'])
        self.assertEqual(api_call.json_string, data['json_string'])
        self.assertEqual(api_call.is_get, data['is_get'])
        self.assertEqual(resp.status_code, 302)

    def test_edit_basic_return_text(self):
        c = Client()
        c.login(username=self.user.email, password=self.password)
        recipe = Recipe.objects.create(
            creator=self.user,
            name='First App',
            description='First Description'
            )

        basic_return_text = BasicReturnText.objects.create(
            return_statement='Hello World!'
            )

        general_action = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text
            )

        general_action.type = 'BT'
        general_action.basic_return_text = basic_return_text
        general_action.recipe = recipe
        general_action.save()
        resp = c.get(reverse('Recipes:edit_basic_return_text',
                     kwargs={'pk': basic_return_text.pk}))
        self.assertEqual(resp.status_code, 200)

        new_return_statement = 'New statement hahahahahaha no copy'
        resp = c.post(reverse('Recipes:edit_basic_return_text',
                      kwargs={'pk': basic_return_text.pk}),
                      {'new_return_statement': new_return_statement}
                      )
        basic_return_text = BasicReturnText.objects.get(
            pk=basic_return_text.pk)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(basic_return_text.return_statement,
                         new_return_statement)


class RecipesModelsTestCases(TestCase):

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

    def test_recipe_insert_action(self):
        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 0)

        self.recipe.insert_action(self.general_action, 0)

        self.general_action = GeneralAction.objects.get(
            pk=self.general_action.pk)

        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 1)

        basic_return_text2 = BasicReturnText.objects.create(
            return_statement='Hello World!2'
            )
        general_action2 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text2
            )

        self.recipe.insert_action(general_action2, 10)

        self.general_action = GeneralAction.objects.get(
            pk=self.general_action.pk)
        general_action2 = GeneralAction.objects.get(
            pk=general_action2.pk)
        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 2)
        self.assertEqual(self.general_action.instruction_number, 1)
        self.assertEqual(general_action2.instruction_number, 2)

        basic_return_text3 = BasicReturnText.objects.create(
            return_statement='Hello World!3'
            )
        general_action3 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text3
            )
        self.recipe.insert_action(general_action3, -10)
        self.general_action = GeneralAction.objects.get(
            pk=self.general_action.pk)
        general_action2 = GeneralAction.objects.get(
            pk=general_action2.pk)
        general_action3 = GeneralAction.objects.get(
            pk=general_action3.pk)
        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 3)
        self.assertEqual(self.general_action.instruction_number, 1)
        self.assertEqual(general_action2.instruction_number, 2)
        self.assertEqual(general_action3.instruction_number, 3)

        basic_return_text4 = BasicReturnText.objects.create(
            return_statement='Hello World!4'
            )
        general_action4 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text4
            )
        self.recipe.insert_action(general_action4, 2)
        self.general_action = GeneralAction.objects.get(
            pk=self.general_action.pk)
        general_action2 = GeneralAction.objects.get(
            pk=general_action2.pk)
        general_action3 = GeneralAction.objects.get(
            pk=general_action3.pk)
        general_action4 = GeneralAction.objects.get(
            pk=general_action4.pk)
        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 4)
        self.assertEqual(self.general_action.instruction_number, 1)
        self.assertEqual(general_action4.instruction_number, 2)
        self.assertEqual(general_action2.instruction_number, 3)
        self.assertEqual(general_action3.instruction_number, 4)

        basic_return_text5 = BasicReturnText.objects.create(
            return_statement='Hello World!5'
            )
        general_action5 = GeneralAction.objects.create(
            type='RT',
            basic_return_text=basic_return_text5
            )
        self.recipe.insert_action(general_action5, 100)
        self.general_action = GeneralAction.objects.get(
            pk=self.general_action.pk)
        general_action2 = GeneralAction.objects.get(
            pk=general_action2.pk)
        general_action3 = GeneralAction.objects.get(
            pk=general_action3.pk)
        general_action4 = GeneralAction.objects.get(
            pk=general_action4.pk)
        general_action5 = GeneralAction.objects.get(
            pk=general_action5.pk)
        number_of_actions = self.recipe.actions.count()
        self.assertEqual(number_of_actions, 5)
        self.assertEqual(self.general_action.instruction_number, 1)
        self.assertEqual(general_action4.instruction_number, 2)
        self.assertEqual(general_action2.instruction_number, 3)
        self.assertEqual(general_action3.instruction_number, 4)
        self.assertEqual(general_action5.instruction_number, 5)

    def test_basic_return_text_action(self):
        next_instruction, return_text = self.basic_return_text.action(1)
        self.assertEqual(next_instruction, 2)
        self.assertEqual(return_text, self.basic_return_text.return_statement)

    def test_general_action_get_action(self):
        next_instruction, return_text = self.general_action.get_action()
        self.assertEqual(next_instruction,
                         self.general_action.instruction_number + 1)
        self.assertEqual(return_text, self.basic_return_text.return_statement)

    def test_conditional_branch(self):
        pass
