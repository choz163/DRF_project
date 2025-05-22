from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from lms.views import CourseRetrieveUpdateDestroyView, SubscriptionAPIView
from lms.models import Course, Subscription


User = get_user_model()


class ForceAuthenticationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='user1@test.com', password='pass')
        self.course = Course.objects.create(title='FA Course', description='desc')
        self.factory = APIRequestFactory()


    def test_subscription_toggle_with_force_authenticate(self):
        view = SubscriptionAPIView.as_view()

        # подписка
        req_sub = self.factory.post(
            '/subscriptions/',
            {'course_id': self.course.id},
            format='json'
        )
        force_authenticate(req_sub, user=self.user)
        resp_sub = view(req_sub)
        self.assertEqual(resp_sub.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_sub.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # отписка
        req_unsub = self.factory.post(
            '/subscriptions/',
            {'course_id': self.course.id},
            format='json'
        )
        force_authenticate(req_unsub, user=self.user)
        resp_unsub = view(req_unsub)
        self.assertEqual(resp_unsub.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_unsub.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())