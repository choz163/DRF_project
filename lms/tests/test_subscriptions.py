from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Subscription


User = get_user_model()


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email = 'user1@test.com', password = 'pass')
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(title='Cx', description='Dx')
        self.url = reverse('subscription')
        self.detail_url = reverse('course-detail', args=[self.course.id])


    def test_subscribe_and_unsubscribe(self):
        # подписка
        resp = self.client.post(self.url, {'course_id': self.course.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
        # отписка
        resp = self.client.post(self.url, {'course_id': self.course.id})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_course_detail_subscription_flag(self):
        # без подписки
        resp = self.client.get(self.detail_url)
        self.assertFalse(resp.data.get('is_subscribed', None))
        # после подписки
        Subscription.objects.create(user=self.user, course=self.course)
        resp = self.client.get(self.detail_url)
        self.assertTrue(resp.data['is_subscribed'])