from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase

from oauth2_provider.models import get_application_model, AccessToken
Application = get_application_model()


from PIL import Image
import tempfile
import json
import os


from django.contrib.auth.models import Group
from users.models import User
from activitie.models import ActivitieParent, ActivitieChild
from gamification.models import Scores
from module.models import Module

class ActivitieCommon(object):
    id = 1
    name = 'hacking activities'
    description = 'description about this activitie'
    die_at = '2015-09-10T01:00'
    file_name = 'activitie/tests/image.jpg'

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


    def _create_module(self):
        from module.serializers import ModuleSerializer
        call_command('Badge')
        self.module = Module(name='Modulo', slug='modulo')
        self.module.save()


    def _create_file(self):
        image = Image.new('RGB', (200, 200), "white")
        image.save(self.file_name)

    def _delete_file(self):
        try:
            os.remove(self.file_name)
        except Exception, e:
            print "file can't be removed"


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

    def _create_activitie(self):
        from django.utils import timezone
        import datetime
        self.activitie = ActivitieParent(
            die_at=timezone.now() + datetime.timedelta(days=1),
            name=self.name,
            description=self.description,
            author=self.user)

        if self.activitie.id != None:
            self.score = Scores(id_event=self.activitie.id, score=10, event="Activity").save()

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
        self._create_module()


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
        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.id, 'slug':self.module.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    """AUTHENTICATED USER"""

    def test_create_activitie_only_name_user_authenticated(self):
        """
        Check Activitie can't be created only with name field and by user authenticated
        """
        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('activitie_parent:activitie_parent_create')
        data = {'name': self.name}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_activitie_all_required_fields_user_authenticated(self):
        """
        Check Activitie can be created by a authenticated user
        """
        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        url = reverse('activitie_parent:activitie_parent_create')
        data = {
            'name': self.name,
            'description': self.description,
            'die_at': self.die_at,
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_activitie_user_authenticated(self):
        """
        Check Activitie can be updated by a authenticated user
        """
        token = self._create_authorization_header(self.user)
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

        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()

        url = reverse('activitie_parent:activitie_parent_update', kwargs={'pk': self.activitie.id, 'slug': self.module.slug})
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
        self._delete_file()
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
        self._delete_file()
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
        token = self._create_authorization_header(self.user)
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
        token = self._create_authorization_header(self.user)
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
            self._delete_file()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_activitie_user_authenticated(self):
        """
        Check Activitie can be updated by a authenticated user
        """
        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()
        self._create_activitie_response(self.activitie)

        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.activitie_response.id})

        self._create_file()

        with open(self.file_name) as file:
            data = {
                'parent': self.activitie.id,
                'file': file
                }

            response = self.client.put(url, data)
            self._delete_file()
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_activitie_user_authenticated(self):
        """
        Check Activitie can be deleted by a authenticated  user
        """
        token = self._create_authorization_header(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=token)

        self._create_activitie()
        self._create_activitie_response(self.activitie)

        url = reverse('activitie_child:activitie_child_update', kwargs={'pk': self.activitie_response.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




class ActivitieChildCheckTests(ActivitieCommon, APITestCase):
    """
    Test class for Activitie Child Ckecks
    """

    def setUp(self):
        self._create_user()
        self._create_user_teacher()
        self._create_application()


    def test_approve_activitie_user_authenticated(self):
            """
            Check Activitie can't be approved by a authenticated user
            """
            token = self._create_authorization_header(self.user)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': self.activitie_response.id})
            data = {
                'action': "approved",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_activitie_user_teacher(self):
            """
            Check Activitie can be approved by a teacher user
            """
            token = self._create_authorization_header(self.user_teacher)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': self.activitie_response.id})
            data = {
                'action': "approved",
                }

            response = self.client.post(url, data)
            self.assertEqual(json.loads(response.content), {'id': self.activitie_response.id, 'msg': 'approved'})
            
    def test_reject_activitie_user_authenticated(self):
            """
            Check Activitie can't be approved by a authenticated user
            """
            token = self._create_authorization_header(self.user)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': self.activitie_response.id})
            data = {
                'action': "rejected",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_activitie_user_teacher(self):
            """
            Check Activitie can be approved by a teacher user
            """
            token = self._create_authorization_header(self.user_teacher)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': self.activitie_response.id})
            data = {
                'action': "rejected",
                }

            response = self.client.post(url, data)
            self.assertEqual(json.loads(response.content), {'id': self.activitie_response.id, 'msg': 'rejected'})

    def test_reject_non_existent_inactivitie_user_teacher(self):
            """
            Check non existent Activitie can't be approved by a teacher user
            """
            token = self._create_authorization_header(self.user_teacher)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': 300})
            data = {
                'action': "rejected",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_approve_non_existent_inactivitie_user_authenticated(self):
            """
            Check Activitie can be approved by a authenticated user
            """
            token = self._create_authorization_header(self.user_teacher)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': 300})
            data = {
                'action': "approved",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_malformed_activitie_user_authenticated(self):
            """
            Check Activitie can be approved by a authenticated user
            """
            token = self._create_authorization_header(self.user_teacher)
            self.client.credentials(HTTP_AUTHORIZATION=token)

            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b','id': self.activitie_response.id})
            data = {
                'action': "approve",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approve_activitie_user_anonymous(self):
            """
            Check Activitie can't be approved by a anonymous user
            """
            self._create_activitie()
            self._create_activitie_response(self.activitie)

            url = reverse('activitie_child:activitie_child_check', kwargs={'mod_slug': 'b', 'id': self.activitie_response.id})
            data = {
                'action': "approved",
                }

            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
