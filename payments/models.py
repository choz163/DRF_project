from django.conf import settings
from django.db import models
from lms.models import Course

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    stripe_product_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    stripe_session_id = models.CharField(max_length=255)
    session_url = models.URLField()
    status = models.CharField(max_length=50, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.pk} for {self.course}"
