from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from degree.views import DegreeList


class RetrieveDegreeTests(APITestCase):
    user = None

    def setUp(self):
        self.user = AnonymousUser()
    
    def test_retrieve_degree(self):
        """
        #Ensure degree can be retrieved by a Anonymous user
        """
        url = reverse('degree-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)