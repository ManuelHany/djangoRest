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
        response = self.client.delete(self.details_url, args=(platform_id,))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


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


class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about="#1 Platform",
                                                           website="https://Netflix.com")
        self.watchlist = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                                         storyline="Example Movie", active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream, title="Example Movie",
                                                         storyline="Example Movie", active=True)
        self.review = models.Review.objects.create(review_user=self.user, rating=5, description="Great Movie",
                                                   watchlist=self.watchlist2, active=True)


    def test_review_create(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(), 2)
        # self.assertEqual(models.Review.objects.get().rating, 5)


        response = self.client.post(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_429_TOO_MANY_REQUESTS])


    def test_review_create_unauth(self):
        data = {
            "review_user": self.user,
            "rating": 5,
            "description": "Great Movie!",
            "watchlist": self.watchlist,
            "active": True
        }

        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('review-create', args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_review_update(self):
        data = {
            "review_user": self.user,
            "rating": 4,
            "description": "Great Movie! - Updated",
            "watchlist": self.watchlist,
            "active": False
        }
        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_review_list(self):
        response = self.client.get(reverse('review-list', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_review_individual(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        user = User.objects.create_user(username="example2", password="Password@123")
        review = models.Review.objects.create(review_user=user, rating=4, description="new Movie",
                                              watchlist=self.watchlist2, active=True)
        review_id = review.id
        token = Token.objects.get(user__username=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        details_url = reverse('review-detail', args=[review_id])
        response = self.client.delete(details_url, args=(review_id,))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username' + self.user.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



