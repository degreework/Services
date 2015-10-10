from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from django.core.management import call_command


from users.models import User

class CreateTests(APITestCase):
    email = 'email@me.to'
    first_name = 'First'
    last_name = 'Last'
    codigo = '00000'
    plan = ''
    password = 'PassWord0'

    def setUp(self):
        call_command('Group')
        call_command('Badge')
        
    def test_create_user_only_email(self):
        """
        Check User can't be registered only with email field
        """
        url = reverse('user_create')
        data = {'email': self.email}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_all_required_fields(self):
        """
        Check User can be registered rightly
        """
        url = reverse('user_create')
        data = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'codigo': self.codigo,
            'password': self.password,
            'plan': self.plan
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RetrieveTests(APITestCase):
    email = 'email@me.to'
    first_name = 'First'
    last_name = 'Last'
    codigo = '00000'
    password = 'PassWord0'
    plan = None

    def setUp(self):
        call_command('Group')
        User.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            codigo=self.codigo,
            password=self.password)

    def test_get_current_no_auth(self):
        """
        A no authenticated User does not have permissions to get current user
        """
        url = reverse('user-current')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_no_auth(self):
        """
        A no authenticated User does not have permissions to retrieve users
        """
        url = reverse('user-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateTests(APITestCase):
    email = 'email@me.to'
    first_name = 'First'
    last_name = 'Last'
    codigo = '00000'
    password = 'PassWord0'
    plan = None


    def setUp(self):
        call_command('Group')
        User.objects.create_user(
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            codigo=self.codigo,
            password=self.password)

    def test_update_no_auth(self):
        """
        A no authenticated User does not have permissions to update a user
        """
        url = reverse('user-update', kwargs={'pk': 1})
        data = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'codigo': '777',
            'password': self.password,
            'plan': self.plan
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_password_no_auth(self):
        """
        A no authenticated User does not have permissions to update password of a user
        """
        url = reverse('user-password', kwargs={'pk': 1})
        data = {
            'old': self.password,
            'new': 'newPass'
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_no_auth(self):
        """
        A no authenticated User does not have permissions to delete a user
        """
        url = reverse('user-update', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class ListTests(APITestCase):


    def test_list_no_auth(self):
        """
        A no authenticated User does not have permissions to list users
        """
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
