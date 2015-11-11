import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.hello.models import Journal, ACTION


@receiver(post_save)
def callback_save(sender, instance=None, created=False, **kwargs):
    if sender.__name__ not in ['Journal', 'Session']:
        action = ACTION[2][1] if created else ACTION[1][1]
        entry = Journal(model_name=sender.__name__,
                        action=action,
                        timestamp=datetime.datetime.now(),
                        id_item=instance.id).save()


@receiver(post_delete)
def callback_delete(sender, instance, signal, *args, **kwargs):
    if sender.__name__ not in ['Journal', 'Session']:
        entry = Journal(model_name=sender.__name__,
                        action=ACTION[0][1],
                        timestamp=datetime.datetime.now(),
                        id_item=instance.id).save()
