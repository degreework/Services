from django.dispatch import receiver
from .models import Request

from .signals import page_request

@receiver(page_request, sender=Request)
def generate_request(sender, page, commit, **kwargs):
    Request(page=page, commit=commit).save()
