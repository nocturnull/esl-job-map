
from .settings import *


class SessionManager:
    """Session manager"""

    @classmethod
    def needs_full_time_warning(cls, request) -> bool:
        """
        Determine if we need to show a warning message for the full time map.

        :param request:
        :return:
        """
        return cls._needs_warning(SESSION_FULL_TIME_WARNING, request)

    @classmethod
    def needs_part_time_warning(cls, request) -> bool:
        """
        Determine if we need to show a warning message for the part time map.

        :param request:
        :return:
        """
        return cls._needs_warning(SESSION_PART_TIME_WARNING, request)

    @staticmethod
    def _needs_warning(key, request) -> bool:
        """
        Check the session for the requested data and set expiry date if nonexistant.

        :param key:
        :param request:
        :return:
        """
        show_warning = False
        # Warning only needed for guest users.
        if not request.user.is_authenticated:
            if key not in request.session:
                request.session[key] = 1
                request.session.set_expiry(60 * 60 * 24 * 7)  # 1 week
                show_warning = True

        return show_warning
