import datetime
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from easy_thumbnails.fields import ThumbnailerImageField

size = (200, 200)

ACTION = (
    ('0', 'delete'),
    ('1', 'edit'),
    ('2', 'create'),
)


class Person(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    birthday = models.DateField(verbose_name='Date of Birth')
    bio = models.TextField(verbose_name='Bio')
    email = models.EmailField(max_length=75, verbose_name='Email')
    jabber = models.CharField(max_length=100, verbose_name='Jabber')
    skype = models.CharField(max_length=100, verbose_name='Skype')
    other = models.TextField(verbose_name='Other contacts')
    photo = ThumbnailerImageField(upload_to='uploads', blank=True, null=True,
                                  resize_source=dict(size=size, sharpen=True))


class Requests(models.Model):
    row = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=250, null=True)
    request_method = models.CharField(max_length=10, null=True)

    def __unicode__(self):
        return str(self.id)


class Journal(models.Model):
    model_name = models.CharField(max_length=25)
    action = models.CharField(choices=ACTION, max_length=1)
    timestamp = models.DateTimeField()
    id_item = models.IntegerField()

    def __unicode__(self):
        return str(self.id)


@receiver(post_save)
def my_callback_save(sender, instance=None, created=False, **kwargs):
    if sender.__name__ not in ['Journal', 'Session']:
        action = ACTION[2][1] if created else ACTION[1][1]
        entry = Journal(model_name=sender.__name__,
                        action=action,
                        timestamp=datetime.datetime.now(),
                        id_item=instance.id)
        entry.save()


@receiver(post_delete)
def my_callback_delete(sender, instance, signal, *args, **kwargs):
    if sender.__name__ not in ['Journal', 'Session']:
        entry = Journal(model_name=sender.__name__,
                        action=ACTION[0][1],
                        timestamp=datetime.datetime.now(),
                        id_item=instance.id)
        entry.save()
