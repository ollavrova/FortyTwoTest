from django.contrib import admin
from apps.hello.models import Person, Requests


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday', 'email', 'skype')


class RequestsAdmin(admin.ModelAdmin):
    list_display = ('id', 'timestamp')


admin.site.register(Person, PersonAdmin)
admin.site.register(Requests, RequestsAdmin)
