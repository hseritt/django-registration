from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationTestCase(TestCase):

	def setUp(self):
		admin_user = User.objects.create(username='admin', email='admin@localhost')
		admin_user.set_password('admin')
		admin_user.save()

	def test_access_registration_app(self):

		c = Client()
		response = c.get('/registration/')
		self.assertEqual(response.status_code, 200)

	def test_post_registration_app_existing_username(self):

		c = Client()
		response = c.post(
			'/registration/',
			{
				'username' : 'admin',
				'email': 'admin@localhost',
			}
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('Username: admin already taken.' in str(response.content))


	def test_post_registration_app_bad_email_format(self):

		c = Client()
		response = c.post(
			'/registration/',
			{
				'username' : 'user1',
				'email': 'user1',
			}
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('Invalid email format: missing @ symbol.' in str(response.content))


	def test_post_registration_app_nonmatching_passwords(self):

		c = Client()
		response = c.post(
			'/registration/',
			{
				'username' : 'user1',
				'email': 'user1@localhost',
				'password': 'admin',
				'password_confirm': 'secret',
			}
		)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('Passwords do not match.' in str(response.content))

	def test_user_creation(self):

		c = Client()
		response = c.post(
			'/registration/',
			{
				'username': 'user1',
				'email': 'user1@localhost',
				'password': 'secret',
				'password_confirm': 'secret',
			}
		)

		user = User.objects.get(username='user1')
		self.assertTrue(user)
		self.assertFalse(user.is_active)

		user_profile = UserProfile.objects.get(user=user)
		self.assertTrue(user_profile)
		self.assertFalse(user_profile.validated)

		response = c.get(
			'/registration/verify/{}'.format(user_profile.ver_code),
			follow=True
		)

		user = User.objects.get(username='user1')
		self.assertTrue(user.is_active)
		
		self.assertEqual(response.redirect_chain[1][0], '/registration/verified/')