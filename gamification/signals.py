import django.dispatch

post_points_quiz = django.dispatch.Signal(providing_args=["sitting"])

post_points_wiki = django.dispatch.Signal(providing_args=["post","request"])

post_points_activity = django.dispatch.Signal(providing_args=["post","request"])