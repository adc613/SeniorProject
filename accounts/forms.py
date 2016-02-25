from django import forms

from .models import User

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password',
		widget = forms.PasswordInput)
	password2 = forms.CharField(label='repeat password',
		widget = forms.PasswordInput)

	class Meta:
		model =	User
		fields = ['email', 'first_name', 'last_name']

    #overrides the clean password method for password2
	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 and password2 and password2 != password1:
			forms.ValidationError('passwords do not match', code='invalid')
		return password2

	def save(self, commit=True):
		user = super(UserCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data['password2'])
		if commit:
			user.save()
		return user
