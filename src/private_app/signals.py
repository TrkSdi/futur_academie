from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """This function automatically creates a user profile when a new user account is made."""
    if created:
        UserProfile.objects.create(user=instance, is_public=False)
