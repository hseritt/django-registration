from django import forms
from django.contrib.auth.models import User

class RegisterUserForm(forms.Form):
	""" Form used for registration.
	"""
	username = forms.CharField(label='Username')
	email = forms.EmailField(label='Email Address')
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password_confirm = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	def clean(self):
		""" Server-side validation for registration form.
		"""
		cleaned_data = super(RegisterUserForm, self).clean()

		username = cleaned_data.get('username')
		try:
			user = User.objects.get(username=username)
			msg = 'Username: {} already taken.'.format(username)
			raise forms.ValidationError(msg)
		except User.DoesNotExist:
			""" This is a good thing.
			"""
			pass

		email = cleaned_data.get('email')
		# Avoiding TypeError: must be str, not NoneType:
		if not email: email = ''
		if '@' not in email:
			msg = 'Invalid email format: missing @ symbol.'
			raise forms.ValidationError(msg)

		password = cleaned_data.get('password')
		password_confirm = cleaned_data.get('password_confirm')

		if password != password_confirm:
			raise forms.ValidationError('Passwords do not match.')
