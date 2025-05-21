from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Lesson
        fields = ['id', 'course', 'name', 'description', 'preview', 'video_url', 'owner']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'preview', 'description',
            'owner', 'lessons_count', 'lessons'
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
