from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson


User = get_user_model()


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email = 'user1@test.com', password = 'pass')
        self.client.force_authenticate(self.user)
        self.course = Course.objects.create(title='C1', description='D1')
        self.lesson = Lesson.objects.create(
            course=self.course, title='L1',
            video_url='https://www.youtube.com/watch?v=abc123',
            content='Text'
            )
        self.list_url = reverse('lesson-list')
        self.detail_url = reverse('lesson-detail', args=[self.lesson.id])


    def test_list_lessons(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('results', resp.data)

    def test_create_lesson_invalid_external(self):
        data = {
            'course': self.course.id,
            'title': 'Bad',
            'video_url': 'https://vimeo.com/123',
            'content': 'X'
        }
        resp = self.client.post(self.list_url, data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', resp.data)


    def test_delete_lesson(self):
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())