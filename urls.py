
from django.conf.urls import url, include
from .views import index, registered, verify, verified, invalid


urlpatterns = [
	url(
		regex=r'^$',
		view=index,
		name='registration_index',
	),
	url(
		regex=r'^registered/$',
		view=registered,
		name='registration_registered',
	),
	url(
		regex=r'^verify/(?P<ver_code>[0-9a-f-]+)/$',
		view=verify,
		name='registration_verify',
	),
	url(
		regex=r'^verified/$',
		view=verified,
		name='registration_verified',
	),
	url(
		regex=r'^invalid/$',
		view=invalid,
		name='registration_invalid',
	),
]