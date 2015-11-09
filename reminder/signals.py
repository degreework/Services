import django.dispatch

forum_answered = django.dispatch.Signal(providing_args=["ask", "answer", "author"])
forum_ask_updated  = django.dispatch.Signal(providing_args=["ask"])

post_comment = django.dispatch.Signal(providing_args=["post", "comment", "author"])

wiki_request_checked = django.dispatch.Signal(providing_args=["request"])
wiki_request_created = django.dispatch.Signal(providing_args=["request"])

gamification_badge_award = django.dispatch.Signal(providing_args=["badge, user"])

create_remove_action = django.dispatch.Signal(providing_args=["author, action, instance"])

create_module = django.dispatch.Signal(providing_args=["author", "module"])

activitie_checked = django.dispatch.Signal(providing_args=["checker", "activitie"])

finish_quiz = django.dispatch.Signal(providing_args=["sitting"])
