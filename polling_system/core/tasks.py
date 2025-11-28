from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Rating  


@shared_task
def send_rating_email(to_email, project_name):
    send_mail(
        subject="Your project received a new rating!",
        message=f"Your project '{project_name}' just got a new rating.",
        from_email="noreply@example.com",
        recipient_list=[to_email],
    )
    return "Email Sent"


@shared_task
def cleanup_old_ratings():
    
    one_week_ago = timezone.now() - timezone.timedelta(days=7)
    count, _ = Rating.objects.filter(created_at__lt=one_week_ago).delete()
    return f"Deleted {count} old ratings."