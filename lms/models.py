from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/')
    video_url = models.URLField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.course.name} - {self.name}"

