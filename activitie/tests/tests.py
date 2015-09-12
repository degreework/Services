from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase

from oauth2_provider.models import get_application_model, AccessToken
Application = get_application_model()


from PIL import Image
import tempfile


from users.models import User
from activitie.models import ActivitieParent, ActivitieChild

class ActivitieCommon(object):
    id = 1
    name = 'hacking activities'
    description = 'description about this activitie'
    die_at = '2015-09-10T01:00'
    file_name = 'image.jpg'

    u_first_name = 'tester'
    u_last_name = 'last_tester'
    u_email = 'testuser@test.com'
    u_codigo = '112233'
    u_password = 'nonsecur3'


    def _create_user(self):
        call_command('Group')
        self.user = User.objects.create_user(
            email=self.u_email,
            first_name=self.u_first_name,
            last_name=self.u_last_name,
            codigo=self.u_codigo,
            password=self.u_password)

    def _create_application(self):
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()


    def _create_file(self):
        image = Image.new('RGB', (200, 200), "white")
        image.save(self.file_name)


    def _create_token(self):
        import datetime
        from django.utils import timezone

        self.token = AccessToken.objects.create(
            user=self.user,
            token='1234567890',
            application=self.application,
            scope='read write',
            expires=timezone.now() + datetime.timedelta(days=1)
            )
        return self.token

    def _create_authorization_header(self, token=None):
        return "Bearer {0}".format(token or self._create_token())

    def _create_activitie(self):
        from django.utils import timezone
        self.activitie = ActivitieParent(
            die_at=timezone.now(),
            name=self.name,
            description=self.description,
            author=self.user)
        self.activitie.save()

    def _create_activitie_response(self, parent):
        self.activitie_response = ActivitieChild(
            parent=parent,
            file=self._create_file(),
            author=self.user)
        self.activitie_response.save()


        

class ActivitieParentTests(ActivitieCommon, APITestCase):
    """
    Test class for ActivitieParent API
    """

    def setUp(self):
        self._create_user()
        self._create_application()


    def test_create_activitie_only_name_user_anonymous(self):
        """
        Check Activitie can't be created only with name field and by anonymous user
        """
        url = reverse('activitie_parent:activitie_parent_create')
        data = {'name': self.name}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_activitie_all_required_fieldsuser_anonymous(self):
        """
        Check Activitie can't be created by a anonymous user
        """
        url = reverse('activitie_parent:activitie_parent_create')
        data = {
            'name': self.name,
            'description': self.description,
            'die_at': self.die_at,
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_activitie_user_anonymous(self):
        """
        Check Activitie can't be updated by a anonymous user
        """
        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.id})
        data = {
            'name': self.name,
            'description': self.description,
            'die_at': self.die_at,
            }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_activitie_user_anonymous(self):
        """
        Check Activitie can't be deleted by a anonymous user
        """
        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    """AUTHENTICATED USER"""

    def test_create_activitie_only_name_user_authenticated(self):
        """
        Check Activitie can't be created only with name field and by user authenticated
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('activitie_parent:activitie_parent_create')
        data = {'name': self.name}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_activitie_all_required_fields_user_authenticated(self):
        """
        Check Activitie can be created by a authenticated user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('activitie_parent:activitie_parent_create')
        data = {
            'name': self.name,
            'description': self.description,
            'die_at': self.die_at,
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_activitie_user_authenticated(self):
        """
        Check Activitie can be updated by a authenticated user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()

        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.activitie.id})
        data = {
            'name': self.name,
            'description': self.name,
            'die_at': self.die_at,
            }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_activitie_user_authenticated(self):
        """
        Check Activitie can be deleted by a authenticated user
        """

        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()

        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.activitie.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)





class ActivitieChildTests(ActivitieCommon, APITestCase):
    """
    Test class for ActivitieChild 
    """

    def setUp(self):
        self._create_user()
        self._create_application()


    def test_create_activitie_only_parent_user_anonymous(self):
        """
        Check Activitie can't be created only with name field and by anonymous user
        """
        url = reverse('activitie_child:activitie_child_create')
        data = {'parent': self.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_activitie_all_required_fieldsuser_anonymous(self):
        """
        Check Activitie can't be created by a anonymous user
        """
        url = reverse('activitie_child:activitie_child_create')

        data = {
            'parent': self.id,
            'file': self._create_file(),
            }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_activitie_user_anonymous(self):
        """
        Check Activitie can't be updated by a anonymous user
        """
        self._create_activitie()
        self._create_activitie_response(self.activitie)

        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.activitie_response.id})
        data = {
            'parent': self.activitie.id,
            'file': self._create_file(),
            }

        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_activitie_user_anonymous(self):
        """
        Check Activitie can't be deleted by a anonymous user
        """
        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    """Test Authenticated user"""

    def test_create_activitie_only_parent_user_authenticated(self):
        """
        Check Activitie can't be created only with name field and by authenticated user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()

        url = reverse('activitie_child:activitie_child_create')
        data = {'parent': self.activitie.id}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_activitie_all_required_fields_user_authenticated(self):
        """
        Check Activitie can be created by a authenticated user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()

        url = reverse('activitie_child:activitie_child_create')

        self._create_file()
        
        with open(self.file_name) as file:
            data = {
                'parent': self.activitie.id,
                'file': file,
                }

            response = self.client.post(url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_activitie_user_authenticated(self):
        """
        Check Activitie can be updated by a authenticated user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()
        self._create_activitie_response(self.activitie)

        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.activitie_response.id})

        with open(self.file_name) as file:
            data = {
                'parent': self.activitie.id,
                'file': file
                }

            response = self.client.put(url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_activitie_user_authenticated(self):
        """
        Check Activitie can be deleted by a authenticated  user
        """
        token = self._create_authorization_header()
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()
        self._create_activitie_response(self.activitie)

        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.activitie_response.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)