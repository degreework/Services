from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class CreateTests(APITestCase):
    email = 'email@me.to'
    first_name = 'First'
    last_name = 'Last'
    codigo = '00000'
    password = 'PassWord0'

    def test_create_user_only_email(self):
        """
        #Check User can't be registered only with email field
        """
        url = reverse('user:user_create')
        data = {'email': self.email}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_all_required_fields(self):
        """
        #Check User can be registered rightly
        """
        url = reverse('user:user_create')
        data = {
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'codigo': self.codigo,
            'password': self.password
            }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)