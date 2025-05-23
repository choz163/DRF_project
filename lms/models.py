from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/")
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Subscription',
        related_name='subscribed_courses',
        blank=True,
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_previews/")
    video_url = models.URLField()
    is_external = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="course_subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
