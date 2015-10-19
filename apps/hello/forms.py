# -*- coding: utf-8 -*-
from apps.hello.widget import CustomDatePicker
from django import forms
from apps.hello.models import Person


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class PersonEditForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'birthday', 'bio', 'email', 'photo', 'skype', 'jabber', 'other']
        widgets = {
            'birthday': CustomDatePicker,
        }

    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if (field == 'bio') or (field == 'other'):
                self.fields[field].widget.attrs['class'] = 'multiline'
                self.fields[field].widget = forms.Textarea(attrs={'rows': 4})
            else:
                self.fields[field].widget.attrs['class'] = 'editform'

