from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.mail_service import ManageMailService
from redis_management.redis_manager import RedisManager


class User(AbstractUser):

    is_active = models.BooleanField(default=False)
    def send_otp_code_to_email(self):
        mail_service = ManageMailService(self.email)
        return mail_service.send_otp_code()

    def verify_user_otp_code(self, raw_otp_code):
        redis_manager = RedisManager(self.email, "Otp_Code")
        if redis_manager.exists():
            if redis_manager.validate(raw_otp_code):
                redis_manager.delete()
                return True
            return False
        return None


