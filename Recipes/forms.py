from django import forms

from .models import (GeneralAction,
                     Recipe,
                     BasicReturnText,
                     APICall,
                     ConditionalHeader)


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


class CreateAPICallForm(forms.ModelForm):
    class Meta:
        model = APICall
        fields = ['is_get', 'url', 'json_string']


class CreateConditonalForm(forms.ModelForm):
    class Meta:
        model = ConditionalHeader
        fields = ['question']


class CreateBranchForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']
