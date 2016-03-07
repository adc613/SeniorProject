from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .forms import CreateActionForm, CreateRecipeForm
from .models import Recipe


class CreateActionView(View):
    template_name = 'create_action.html'
    form = CreateActionForm

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        context['form'] = self.form

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            recipe = Recipe.objects.get(pk=kwargs['recipe_pk'])
            if recipe.creator == request.user:
                model.recipe = recipe
                model.save()
            else:
                return HttpResponseRedirect(reverse('accounts:login'))

        return HttpResponseRedirect(reverse('Recipes:create_action'))


class CreateRecipeView(View):
    template_name = 'create_recipe.html'
    form = CreateRecipeForm

    @method_decorator(login_required)
    def get(self, request):
        context = {}
        context['form'] = self.form

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse('Recipes:create_recipe'))
