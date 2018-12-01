# employment/managers/apply_manager.py


class ApplyManager:
    """Apply related tasks manager"""

    @staticmethod
    def resolve_success_text(referer) -> str:
        """
        Show the relevant message when the user has finished applying.

        :param referer:
        :return: str
        """
        if 'full-time/seoul' in referer:
            text = 'Apply to more Full-Time jobs in Seoul'
        elif 'full-time/busan' in referer:
            text = 'Apply to more Full-Time jobs in Busan'
        elif 'full-time' in referer:
            text = 'Apply to more Full-Time jobs'
        elif 'part-time/seoul' in referer:
            text = 'Apply to more Part-Time jobs in Seoul'
        elif 'part-time/busan' in referer:
            text = 'Apply to more Part-Time jobs in Busan'
        else:
            text = 'Apply to more Part-Time jobs'

        return text
