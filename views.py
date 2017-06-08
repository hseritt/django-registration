from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .forms import RegisterUserForm
from .messages import REGISTRATION_FORM_LEGEND, FOOTER_TEXT, INVALID_MSG, REGISTERED_MSG, VERIFIED_MSG
from .models import UserProfile
from .settings import VERIFICATION_URL, REGISTRATION_EMAIL_MSG, REGISTRATION_EMAIL_SUBJ, EMAIL_FROM


def create_user(form):
	""" Creates a user object from the registration form.
	"""
	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password']
	user = User.objects.create(username=username, email=email)
	user.set_password(password)
	user.is_active = False
	user.save()
	return user


def send_email(email, verification_code):
	""" Sends email with verification link to registered user.
	"""
	url = VERIFICATION_URL + str(verification_code)
	message = REGISTRATION_EMAIL_MSG % (url,)
	send_mail(REGISTRATION_EMAIL_SUBJ, message, EMAIL_FROM, [email,], fail_silently=False)
	

def index(request):
	""" View: /
	"""
	if request.method == 'GET':
		register_user_form = RegisterUserForm()

	if request.method == 'POST':
		register_user_form = RegisterUserForm(request.POST)
		if register_user_form.is_valid():
			user = create_user(register_user_form)
			user_profile = UserProfile.objects.create(user=user)
			send_email(user.email, user_profile.ver_code)
			return HttpResponseRedirect(reverse('registration_registered'))


	return render(
		request,
		'registration/index.html',
		{
			'register_user_form': register_user_form,
			'fieldset_legend': REGISTRATION_FORM_LEGEND,
			'footer_text': FOOTER_TEXT,
		},
	)


def registered(request):
	""" View: /registered/ Prints message to user that he/she is registered.
	"""
	return render(
		request,
		'registration/registered.html',
		{
			'registered_msg': REGISTERED_MSG,
		}
	)


def verified(request):
	""" View: /verified/ Prints email verified message to registered user.
	"""
	return render(
		request,
		'registration/verified.html',
		{
			'verified_msg': VERIFIED_MSG,
		}
	)


def invalid(request):
	""" View: /invalid/ Prints invalid verification code message to user.
	"""
	return render(
		request,
		'registration/invalid.html',
		{
			'invalid_msg': INVALID_MSG,
		}
	)


def verify(request, ver_code):
	""" View: /verify/<ver_code>/ Attempts verification of email address.
	"""
	try:
		user_profile = UserProfile.objects.get(ver_code=ver_code)
		user_profile.validated = True
		user_profile.validation_date = timezone.now()
		user_profile.save()
		user = user_profile.user
		user.is_active = True
		user.save()
		return HttpResponseRedirect(reverse('registration_verified'))

	except UserProfile.DoesNotExist:
		return HttpResponseRedirect(reverse('registration_invalid'))
