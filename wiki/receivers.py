from django.dispatch import receiver
from .models import Request

from .signals import page_request

@receiver(page_request, sender=Request)
def generate_request(sender, page, commit, author, **kwargs):
    Request(page=page, commit=commit, checked_by=None, created_by=author).save()
