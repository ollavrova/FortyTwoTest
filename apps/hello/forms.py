# -*- coding: utf-8 -*-
import datetime
from apps.hello.widget import CustomDatePicker
from django import forms
from apps.hello.models import Person


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            'birthday': CustomDatePicker(
                params="dateFormat: 'yy-mm-dd', changeYear: true, defaultDate: '-37y', yearRange: 'c-15:c+15'",  # NOQA
                attrs={'type': 'date'},
            )
        }

    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['type'] = 'email'
        for field in self.fields:
            if (field == 'bio') or (field == 'other'):
                self.fields[field].widget.attrs['class'] = 'multiline'
                self.fields[field].widget = forms.Textarea(attrs={'rows': 4})
            else:
                self.fields[field].widget.attrs['class'] = 'editform'

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday >= datetime.datetime.now().date():
            raise forms.ValidationError("You must input date before today!")
        return birthday
