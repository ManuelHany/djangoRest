from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatformTestCase(APITestCase):


    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.admin_user = User.objects.create_user(username="staff_example", password="StaffPassword@123",
                                                   is_staff=True, is_superuser=True)
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://Netflix.com")
        self.list_url = reverse('streamplatform-list')
        self.details_url = reverse('streamplatform-detail', args=[self.stream.id])


    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://netflix.com"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_individual(self):
        response = self.client.get(self.details_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_update_admin(self):
        data = {
            "name": "Netflix",
            "about": "mousa nageh",
            "website": "https://www.netflix.com"
        }
        self.token = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(self.details_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.StreamPlatform.objects.get(id=self.stream.id).about, data['about'])


    def test_stream_platform_update(self):
        data = {
            "name": "Netflix",
            "about": "mousa mesh nageh",
            "website": "https://www.netflix.com"
        }
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(self.details_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stream_platform_delete_admin(self):
        platform_id = self.stream.id
        self.token = self.token = Token.objects.get(user__username=self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        print(f"platform: {self.stream}\nid: {platform_id}")
        response = self.client.delete(self.details_url, args=(platform_id,))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.mostafa = 3
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://Netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                                         storyline="Example Movie", active=True)
    def test_watchlist_create(self):
        data = {
            "platform": self.stream,
            "title": "Example Movie",
            "storyline": "Example Story",
            "active": True
        }
        response = self.client.post(reverse('movie-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_individual(self):
        response = self.client.get(reverse('movie-detail', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')
