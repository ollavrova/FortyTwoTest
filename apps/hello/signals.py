from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.hello.models import Journal

models_list = ['Journal', 'Session']


@receiver(post_save)
def callback_save(sender, instance=None, created=False, **kwargs):
    if sender.__name__ not in models_list:
        action = Journal.CREATED_STATUS if created else Journal.EDITED_STATUS
        Journal(model_name=sender.__name__,
                action=action,
                id_item=instance.id).save()


@receiver(post_delete)
def callback_delete(sender, instance, signal, *args, **kwargs):
    if sender.__name__ not in models_list:
        Journal(model_name=sender.__name__,
                action=Journal.DELETED_STATUS,
                id_item=instance.id).save()
