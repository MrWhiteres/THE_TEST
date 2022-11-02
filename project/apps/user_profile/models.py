"""
This module contains all models for db
"""
from django.contrib.auth.models import User
from django.db.models import Model, OneToOneField, CASCADE, ImageField, CharField, TextField
from django.db.models.signals import post_save
from django.dispatch import receiver


def path_to_img(instance, filename):
    return f"avatar_user/avatar{instance.user}){filename[-4:]}"


class UserProfile(Model):
    user = OneToOneField(User, related_name='profile', on_delete=CASCADE)
    avatar_urls = TextField(max_length=1000)
    avatar = ImageField(upload_to=path_to_img)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        """
        Change name model in admin panel.
        """

        verbose_name = "User Profile"
        verbose_name_plural = 'User Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
