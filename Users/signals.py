from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser

@receiver(post_save, sender=CustomUser, dispatch_uid="send_welcome_email")
def send_welcome_email(sender, instance, created, **kwargs):
    print(f"Signal triggered for {instance.username} with created={created}")
    if created:
        send_mail(
            "Welcome!",
            "Thank you for registering with ProductShop. We are glad to have you!",
            "admin@django.com",
            [instance.email],
            fail_silently=False,
        )
        print(f"Welcome email sent to {instance.email}")
        # You can use Django's EmailMessage or any other email sending library here
