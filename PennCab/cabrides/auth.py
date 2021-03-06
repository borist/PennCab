from cabrides.models import CabUser

"""
Need to define custom user authentication since we used a customer User class
for the project
"""
class CustomAuth(object):
    def authenticate(self, username=None, password=None):
        try:
            user = CabUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except CabUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CabUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except CabUser.DoesNotExist:
            return None
