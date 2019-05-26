# account/authbackend.py

from .models.user import SiteUser


class UserAccountBackend:
    """
    Custom backend auth service.
    """

    def authenticate(self, request, username=None, password=None):
        try:
            # Ignore email case.
            user = SiteUser.objects.get(email__iexact=username.lower())
            if user.check_password(password):
                return user
        except SiteUser.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None
