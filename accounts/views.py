from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from .forms import UserCreationForm


class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class ItWorkedView(View):
    template_name = 'itworked.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


class CreateAccountView(View):
    template_name = 'create_account.html'
    form = UserCreationForm

    def get(self, request):
        context = {}
        context['form'] = self.form
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:it_worked'))

        return HttpResponseRedirect(reverse('home'))


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:it_worked'))

        return HttpResponseRedirect(reverse('home'))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
