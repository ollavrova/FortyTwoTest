from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField


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
                                  resize_source=dict(size=(200, 0),
                                                     crop='scale',
                                                     autocrop=True,
                                                     upscale=True))


class Requests(models.Model):
    row = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    request_path = models.CharField(max_length=250, null=True)
    request_method = models.CharField(max_length=10, null=True)
    priority = models.IntegerField(default=1)

    def __unicode__(self):
        return str(self.id)


class Journal(models.Model):
    model_name = models.CharField(max_length=25)
    action = models.CharField(choices=(('0', 'delete'),
                                       ('1', 'edit'),
                                       ('2', 'create'),
                                       ), max_length=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    id_item = models.IntegerField()

    def __unicode__(self):
        return str(self.id)
