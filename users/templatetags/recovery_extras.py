from django import template
from django.conf import settings

register = template.Library()

# settings value
@register.simple_tag
def get_url_confirm_password():
    return getattr(settings, "SITE_CLIENT_URL_CONFIRM_PASSWORD_RECOVERY", "")


@register.simple_tag
def get_site_name():
    return getattr(settings, "SITE_CLIENT_NAME", "")