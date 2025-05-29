from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_course_update_email(course_id, user_email):
    subject = 'Курс обновлён!'
    message = f'У курса с id={course_id} появились новые материалы. Загляните в личный кабинет.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    cutoff = timezone.now() - timedelta(days=30)
    qs = User.objects.filter(is_active=True, last_login__lt=cutoff)
    count = qs.update(is_active=False)
    return f'Deactivated {count} users'