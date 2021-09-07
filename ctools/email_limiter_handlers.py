import logging
from django.conf import settings
from django.utils.log import AdminEmailHandler
from django.core.cache import cache


logger = logging.getLogger(__name__)


class ThrottledAdminEmailHandler(AdminEmailHandler):
    COUNTER_CACHE_KEY = "email_admins_counter"
    ADMIN_EMAIL_COUNTER_TIMEOUT = getattr(
        settings, 'ADMIN_EMAIL_COUNTER_TIMEOUT', 30)
    ADMIN_EMAIL_COUNTER_MAX = getattr(settings, 'ADMIN_EMAIL_COUNTER_MAX', 10)

    def increment_counter(self):
        try:
            cache.incr(self.COUNTER_CACHE_KEY)
        except ValueError:
            cache.set(self.COUNTER_CACHE_KEY, 1,
                      self.ADMIN_EMAIL_COUNTER_TIMEOUT)
        return cache.get(self.COUNTER_CACHE_KEY)

    def emit(self, record):
        try:
            counter = self.increment_counter()
        except Exception:
            pass
        else:
            if counter > self.ADMIN_EMAIL_COUNTER_MAX:
                logger.error(
                    f"admin email reach to max:{self.ADMIN_EMAIL_COUNTER_MAX:}")
                return
        super().emit(record)
