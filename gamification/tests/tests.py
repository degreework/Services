from django.core.urlresolvers import reverse

from rest_framework import status
from rest_framework.test import APITestCase

class VotesTests(APITestCase):
    """
    Test class for Votes API
    """


    def test_give_vote_user_anonymous(self):
        """
        Check Vote can't be give by anonymous user
        """
        url = reverse('votes:vote-give')
        data = {
            'thread': 1,
            'vote': 1
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_list_thread_votes_user_anonymous(self):
        """
        Check Thread's Votes can't be listing by anonymous user
        """
        url = reverse('votes:vote-detail', kwargs={'pk': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
