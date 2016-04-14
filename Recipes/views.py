from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View

from .forms import CreateActionForm, CreateRecipeForm,\
    CreateBasicReturnTextForm, CreateAPICallForm, CreateConditonalForm, \
    ConditionalHeader, CreateBranchForm
from .models import Recipe, BasicReturnText, GeneralAction


class CreateActionView(View):
    template_name = 'Recipes/create_action.html'
    form = CreateActionForm

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        context = {}
        context['form'] = self.form
        context['recipe'] = Recipe.objects.get(pk=kwargs['recipe_pk'])
        context['actions'] = context['recipe'].actions.all().order_by(
            'instruction_number')

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            recipe = Recipe.objects.get(pk=kwargs['recipe_pk'])

            if recipe.get_user() == request.user:
                model.recipe = recipe
            else:
                return HttpResponseRedirect(reverse('accounts:login'))

            if model.type == 'RT':
                form = CreateBasicReturnTextForm(request.POST)
                if form.is_valid():
                    action = form.save()
                    model.basic_return_text = action
                    model = recipe.add_action(model)
                    model.save()
            elif model.type == 'C':
                form = CreateConditonalForm(request.POST)
                if form.is_valid():
                    conditional = form.save()
                    model.conditional = conditional
                    conditional.save()
                    model.save()
                    model = recipe.add_action(model)

        url = reverse('Recipes:create_action', kwargs=kwargs)
        return HttpResponseRedirect(url)


class CreateRecipeView(View):
    template_name = 'Recipes/create_recipe.html'
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
            model = form.save(commit=False)
            model.creator = request.user
            model.save()

        return HttpResponseRedirect(reverse('Recipes:create_action',
                                            kwargs={'recipe_pk': model.pk}))


class EditBasicReturnTextView(View):
    template_name = 'Recipes/edit_basic_return_text.html'

    @method_decorator(login_required)
    def get(self, request, **kwargs):
        context = {}
        context['model'] = BasicReturnText.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        model = BasicReturnText.objects.get(pk=kwargs['pk'])
        if model.general_action.recipe.creator == request.user:
            model.return_statement = request.POST['new_return_statement']
            model.save()
        return HttpResponseRedirect(reverse('Recipes:edit_basic_return_text',
                                    kwargs=kwargs))


class AddAPICallView(View):
    """
    View for adding an api call to a general action
    """
    template_name = 'Recipes/add_api_call.html'
    form = CreateAPICallForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        model = GeneralAction.objects.get(pk=kwargs['pk'])
        if model.recipe.creator == request.user:
            context['model'] = model

        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        model = GeneralAction.objects.get(pk=kwargs['pk'])
        if model.recipe.creator == request.user:
            form = self.form(request.POST)
            if form.is_valid():
                api_call = form.save()
                model.api_call = api_call
                model.is_api_call = True
                model.save()

        return HttpResponseRedirect(reverse('Recipes:add_api_call',
                                    kwargs=kwargs))


class AddConditionalBranchView(View):
    """
    View for adding a conditional
    """
    template_name = 'Recipes/add_conditional_branch.html'
    form = CreateBranchForm

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = {}
        conditional_header = ConditionalHeader.objects.get(pk=kwargs['pk'])
        if not (conditional_header.get_user() == request.user):
            return HttpResponseRedirect(reverse('accounts:login'))
        context['conditional_header'] = conditional_header
        context['branches'] = conditional_header.get_branches()
        return render(request, self.template_name, context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        conditional_header = ConditionalHeader.objects.get(pk=kwargs['pk'])
        if not (conditional_header.get_user() == request.user):
            return HttpResponseRedirect(reverse('accounts:login'))

        if form.is_valid():
            branch = form.save(commit=False)
            branch.parent_header = conditional_header
            branch.is_conditional_branch = True
            conditional_header.add_branch(branch)
            conditional_header.save()
            branch.save()

        return HttpResponseRedirect(reverse('Recipes:add_conditional_branch',
                                            kwargs=kwargs))
