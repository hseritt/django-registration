""" See:
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
"""
import uuid
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

	user = models.OneToOneField(User,  on_delete=models.CASCADE)
	validated = models.BooleanField(default=False)
	validation_date = models.DateTimeField(null=True, blank=True)
	ver_code = models.UUIDField(default=uuid.uuid4, editable=False)

	def __str__(self):
		return self.user.username
