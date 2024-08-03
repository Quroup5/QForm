from django.contrib.auth import models
from utils.mail_service import ManageMailService
from redis_management.redis_manager import RedisManager


class User(models.AbstractUser):

    def send_otp_code_to_email(self):
        mail_service = ManageMailService(self.email)
        return mail_service.send_otp_code()

    def verify_user_otp_code(self, raw_otp_code):
        redis_manager = RedisManager(self.email, "Otp_Code")
        if redis_manager.validate(raw_otp_code):
            redis_manager.delete()
            return True
        return False
