from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models.users import User

class Profile(models.Model):
    first_name = models.CharField(max_length=42)
    last_name = models.CharField(max_length=42)
    country = models.CharField(max_length=21)
    phone = models.CharField(max_length=21)
    created_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)