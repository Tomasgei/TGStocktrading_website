import logging
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from accounts.tokens import account_activation_token

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from celery import shared_task
from core import settings
from portfolio.models import Portfolio

import logging
logger = logging.getLogger(__name__)

@shared_task(bind=True)
def send_mail_func(self):
    logger.info("Celery krok 1")
    #operations
    user = get_user_model().objects.get(pkid=3)

    send_mail(
    "Subject here",
    "Here is the message.",
    "from@example.com",
    ["geissler.tomas@gmail.com"],
    fail_silently=True,
    )

