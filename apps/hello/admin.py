from django.contrib import admin
from apps.hello.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthday',
                    'email', 'skype', 'jabber')


admin.site.register(Person, PersonAdmin)
