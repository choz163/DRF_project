from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import validate_no_external_links

class LessonSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    owner = serializers.ReadOnlyField(source="owner.username")
    video_url = serializers.URLField(validators=[validate_no_external_links])

    class Meta:
        model = Lesson
        fields = [
            "id",
            "course",
            "title",
            "description",
            "preview",
            "video_url",
            "owner",
            "content",
        ]
        read_only_fields = ("id",)


class CourseSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    preview = serializers.ImageField(read_only=True)
    description = serializers.CharField()
    owner = serializers.ReadOnlyField(source="owner.username")
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "owner",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]
        read_only_fields = ("id", "is_subscribed")

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False
        return obj.subscribers.filter(pk=request.user.pk).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("id", "user", "course")
