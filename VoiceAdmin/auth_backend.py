from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from VoiceAdmin.user_access import ALLOWED_USERS

class ConfBackend(object):

	def authenticate(self, username=None, password=None):
		login_valid = (username in ALLOWED_USERS)

		if login_valid:
			pwd_valid = (ALLOWED_USERS[username]['passwd'] == password)
		else:
			pwd_valid = False
			
		if login_valid and pwd_valid:
			try:
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				user = User(username=username, password='get from settings.py')
				user.save()
			return user
		return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
