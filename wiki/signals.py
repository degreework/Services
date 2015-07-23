import django.dispatch

page_request = django.dispatch.Signal(providing_args=["page", "commit"])
