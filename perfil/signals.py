from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Si es un usuario nuevo, crea el perfil (o lo obtiene si ya existe)
        Profile.objects.get_or_create(user=instance)
    else:
        # Si es un usuario existente, verifica si tiene perfil antes de guardarlo
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            # Si no tiene perfil, créalo
            Profile.objects.get_or_create(user=instance)