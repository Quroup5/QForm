from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from redis_management.redis_manager import RedisManager


class ManageMailService:

    def __init__(self, receiver_email):
        self.receiver_email = receiver_email

    def send_email_to_user(self, subject, content):
        target_email = self.receiver_email
        html_content = render_to_string("email_template/email.html", {"content": content})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [target_email])
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True

    def send_otp_code(self, **kwargs):
        redis_manager = RedisManager(self.receiver_email,"Otp_Code")
        otp_code = redis_manager.create_and_set_otp_key()
        content = {"title": "Your OTP code", "message": otp_code}
        self.send_email_to_user("Your OTP code", content)
        return otp_code
