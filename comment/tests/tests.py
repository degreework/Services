from django.core.urlresolvers import reverse
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APITestCase


class CommentTests(APITestCase):
    """
    Test class for Comment API
    """

    """ANONYMOUS USER"""

    def test_create_comment_user_anonymous(self):
        """
        Check Comment can't be created by anonymous user
        """
        url = reverse('comment:comment-create')
        data = {
            'parent': 1,
            'text': 'my comment'
            }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_comment_user_anonymous(self):
        """
        Check Comment can't be listing by anonymous user
        """
        url = reverse('comment:comment-list', kwargs={'thread': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)