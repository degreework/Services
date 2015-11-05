from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase

from oauth2_provider.models import get_application_model, AccessToken
Application = get_application_model()



from django.contrib.auth.models import Group
from users.models import User

from material.models import Material

class MaterialCommon(object):
    id = 1
    title = 'hacking material'
    description = 'description about this Material'
    link = 'http://g4.local:8080/admin/badger/badge/'

    u_first_name = 'tester'
    u_last_name = 'last_tester'
    u_email = 'testuser@test.com'
    u_codigo = '112233'
    u_password = 'nonsecur3'


    #Teacher User
    u_t_first_name = 'teacher'
    u_t_last_name = 'last_teacher'
    u_t_email = 'teacher@test.com'
    u_t_codigo = '000000'


    #Student User
    u_s_first_name = 'student'
    u_s_last_name = 'last_student'
    u_s_email = 'student@test.com'
    u_s_codigo = '000001'


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

    def _create_user_Student(self):
        call_command('Group')
        self.user_student = User.objects.create_user(
            email=self.u_s_email,
            first_name=self.u_s_first_name,
            last_name=self.u_s_last_name,
            codigo=self.u_s_codigo,
            password=self.u_password)

        g = Group.objects.get(name='Registered') 
        g.user_set.add(self.user_student)

    def _create_application(self):
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()


    def _create_ask(self):
        pass


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

        

class MaterialTests(MaterialCommon, APITestCase):
    """
    Test class for Material API
    """

    def setUp(self):
        self._create_user()
        self._create_user_Student()
        self._create_user_teacher()
        self._create_application()


    """ANONYMOUS USER"""

    def test_create_material_user_anonymous(self):
        """
        Check Material can't be created by anonymous user
        """
        url = reverse('material:material_create')
        data = {
            'title': self.title,
            'description': self.description,
           	'url': self.link
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_get_material_user_anonymous(self):
        """
        Check Material can't be retrieve by a anonymous user
        """

        url = reverse('material:material_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    """AUTHENTICATED USER (Student)"""

    def test_create_material_user_authenticated_as_Student(self):
        """
        Check Material can't be created by user authenticated as Student
        """
        token = self._create_authorization_header(self.user_student)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('material:material_create')
        data = {
            'title': self.title,
            'description': self.description,
           	'url': self.link
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_material_user_authenticated_as_Student(self):
        """
        Check Material can be retrieve by a authenticated user as Student
        """
        token = self._create_authorization_header(self.user_student)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('material:material_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    """AUTHENTICATED USER (Teacher)"""

    def test_create_material_user_authenticated_as_Teacher(self):
        """
        Check Material can be created by user authenticated as Teacher
        """
        token = self._create_authorization_header(self.user_teacher)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('material:material_create')
        data = {
            'title': self.title,
            'description': self.description,
           	'url': self.link
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_material_user_authenticated_as_Teacher(self):
        """
        Check Material can be retrieve by a authenticated user as Teacher
        """
        token = self._create_authorization_header(self.user_teacher)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('material:material_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    