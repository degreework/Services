from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase

from oauth2_provider.models import get_application_model, AccessToken
Application = get_application_model()



from django.contrib.auth.models import Group
from users.models import User


class NotificationCommon(object):
    u_first_name = 'tester'
    u_last_name = 'last_tester'
    u_email = 'testuser@test.com'
    u_codigo = '112233'
    u_password = 'nonsecur3'


    u_t_first_name = 'teacher'
    u_t_last_name = 'last_teacher'
    u_t_email = 'teacher@test.com'
    u_t_codigo = '000000'


    def _create_user(self):
        call_command('Group')
        self.user = User.objects.create_user(
            email=self.u_email,
            first_name=self.u_first_name,
            last_name=self.u_last_name,
            codigo=self.u_codigo,
            password=self.u_password)

    def _create_user_teacher(self):
        call_command('Group')
        self.user_teacher = User.objects.create_user(
            email=self.u_t_email,
            first_name=self.u_t_first_name,
            last_name=self.u_t_last_name,
            codigo=self.u_t_codigo,
            password=self.u_password)
        g = Group.objects.get(name='Teacher') 
        g.user_set.add(self.user_teacher)

    def _create_application(self):
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

    def _create_token(self, user):
        import datetime
        from django.utils import timezone

        self.token = AccessToken.objects.create(
            user=user,
            token= u"%s1234567890" % user.id,
            application=self.application,
            scope='read write',
            expires=timezone.now() + datetime.timedelta(days=1)
            )
        return self.token

    def _create_authorization_header(self, user, token=None):
        return "Bearer {0}".format(token or self._create_token(user))




class NotificationTests(APITestCase, NotificationCommon):
    """
    Test class for Notification API
    """

    def setUp(self):
        self._create_user()
        self._create_application()

    def test_anonymous_user(self):
        """Check non authenticated user can't get feed notification"""
        url = reverse('notification')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_authenticated_user(self):
        """Check authenticated user can get feed notifications"""
        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('notification')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)