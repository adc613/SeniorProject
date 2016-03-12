from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from accounts.models import User


class AccountsViewsTestCases(TestCase):

    def test_home_page_view(self):
        c = Client()
        resp = c.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_create_account_view(self):
        c = Client()
        resp = c.get(reverse('accounts:create_account'))
        self.assertEqual(resp.status_code, 200)

        first_name = 'testcasename'

        resp = c.post(reverse('accounts:create_account'), {
            'email': 'adc82@case.edu',
            'first_name': first_name,
            'last_name': 'Collins',
            'password1': '$tr0ngPa$$worD',
            'password2': '$tr0ngPa$$worD'
            })

        self.assertEqual(resp.status_code, 302)
        user = User.objects.get(pk=1)
        self.assertEqual(user.first_name, first_name)

        resp = c.post(reverse('accounts:create_account'), {
            'email': 'adc82@case.edu',
            'first_name': 'Adam',
            'last_name': 'Collins',
            'password1': '$tr0ngPa$$worD',
            'password2': 'not a matching password'
            })
        self.assertEqual(resp.status_code, 200)

    def test_login_and_logout_view(self):
        email = 'adc82@case.edu'
        password = '$tr0ngPa$$worD'
        user = User.objects.create_user(email=email, password=password)

        c = Client()
        resp = c.get(reverse('accounts:login'))
        self.assertEqual(resp.status_code, 200)

        resp = c.post(reverse('accounts:login'), {
            'username': email,
            'password': password
            })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(int(c.session['_auth_user_id']), user.pk)

        resp = c.get(reverse('accounts:logout'))
        self.assertEqual(resp.status_code, 302)

        resp = c.post(reverse('accounts:login'), {
            'username': email,
            'password': 'wrong password'
            })
        self.assertEqual(resp.status_code, 200)

    def test_link_echo_to_user_view(self):
        c = Client()

        resp = c.get(reverse('accounts:link_echo_to_user'))
        self.assertEqual(resp.status_code, 200)
