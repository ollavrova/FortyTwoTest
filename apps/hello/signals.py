from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.hello.models import Journal

models_list = ['Journal', 'Session']


@receiver(post_save)
def callback_save(sender, instance=None, created=False, **kwargs):
    if sender.__name__ not in models_list:
        action = 'create' if created else 'edit'
        entry = Journal(model_name=sender.__name__,
                        action=action,
                        id_item=instance.id).save()


@receiver(post_delete)
def callback_delete(sender, instance, signal, *args, **kwargs):
    if sender.__name__ not in models_list:
        entry = Journal(model_name=sender.__name__,
                        action='delete',
                        id_item=instance.id).save()
