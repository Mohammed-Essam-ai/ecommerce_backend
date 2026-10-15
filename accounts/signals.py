from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import *

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_token(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
