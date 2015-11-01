import django.dispatch


page_request = django.dispatch.Signal(providing_args=["new_title", "page", "commit", "author", "message"])
