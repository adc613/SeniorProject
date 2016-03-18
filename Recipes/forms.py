from django import forms

from .models import GeneralAction, Recipe, BasicReturnText


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['description', 'name']


class CreateActionForm(forms.ModelForm):
    class Meta:
        model = GeneralAction
        fields = ['type']


class CreateBasicReturnTextForm(forms.ModelForm):
    class Meta:
        model = BasicReturnText
        fields = ['return_statement']
