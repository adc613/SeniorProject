from django import forms

from .models import GeneralAction, Recipe


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['description', 'name']


class CreateActionForm(forms.ModelForm):
    class Meta:
        model = GeneralAction
        fields = ['return_statement', 'type']
