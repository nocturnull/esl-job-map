# employment/model_attributes/localize.py

from pytz import timezone

local_timezone = timezone('Asia/Seoul')  # Change to system env later on...


class Localize:

    @property
    def local_created_at(self):
        """
        Converts the create date (in UTC) to a local timezone.

        :return:
        """

        return self.created_at.astimezone(local_timezone)

    @property
    def local_date_joined(self):
        """
        Converts the date joined (in UTC) to a local timezone.

        :return:
        """
        return self.date_joined.astimezone(local_timezone)
