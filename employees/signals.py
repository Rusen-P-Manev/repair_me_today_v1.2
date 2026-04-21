from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Employee


@receiver(post_save, sender=Employee)
def assign_user_to_group(sender, instance, created, **kwargs):
    if instance.user:

        instance.user.groups.clear()

        manager_titles = [
            'управител', 'собственик',
            'директор', 'администратор',
            'manager', 'owner'
        ]

        is_manager = any(title in instance.position.lower() for title in manager_titles)

        if is_manager:
            group, _ = Group.objects.get_or_create(name='Managers')
        else:
            group, _ = Group.objects.get_or_create(name='Mechanics')

        instance.user.groups.add(group)