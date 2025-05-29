from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.utils import timezone
from datetime import timedelta

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .tasks import send_course_update_email


course_id_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['course_id'],
    properties={
        'course_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID курса')
    }
)


message_response = openapi.Response(
    description='Результат операции',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'message': openapi.Schema(type=openapi.TYPE_STRING)}
    )
)



class LessonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50



class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



    @swagger_auto_schema(
        operation_description="Подписаться на курс. Если уже подписаны — вернёт 400.",
        responses={
            201: SubscriptionSerializer,
            400: '{"detail": "Уже подписаны"}'
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        course = self.get_object()
        sub, created = Subscription.objects.get_or_create(user=request.user, course=course)
        if not created:
            return Response({'detail': 'Уже подписаны'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Отписаться от курса. Если не были подписаны — вернёт 400.",
        responses={
            204: 'No Content',
            400: '{"detail": "Не подписаны"}'
        }
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unsubscribe(self, request, pk=None):
        course = self.get_object()
        sub = Subscription.objects.filter(user=request.user, course=course).first()
        if not sub:
            return Response({'detail': 'Не подписаны'}, status=status.HTTP_400_BAD_REQUEST)
        sub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        prev_updated = course.updated_at

        serializer = self.get_serializer(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


        now = timezone.now()
        if now - prev_updated >= timedelta(hours=4):
            for user in course.subscribers.all():
                send_course_update_email.delay(course.id, user.email)

        return Response(serializer.data, status=status.HTTP_200_OK)



class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LessonPagination


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=course_id_schema,
        responses={200: message_response, 404: 'Course not found'}
    )
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        qs = Subscription.objects.filter(user=user, course=course)
        if qs.exists():
            qs.delete()
            return Response({'message': 'подписка удалена'}, status=status.HTTP_200_OK)
        else:
            Subscription.objects.create(user=user, course=course)
            return Response({'message': 'подписка добавлена'}, status=status.HTTP_200_OK)
