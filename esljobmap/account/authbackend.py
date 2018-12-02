# account/authbackend.py

from .models.user import SiteUser


class UserAccountBackend:
    """
    Backend auth service to track session data.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            user = SiteUser.objects.get(email__iexact=username.lower())
            if user.check_password(password):
                request.session['email'] = user.email
                return user
        except SiteUser.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None
