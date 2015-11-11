from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import DateInput
from fortytwo_test_task.settings import STATIC_URL


class CustomDatePicker(DateInput):
    def __init__(self, params='', attrs=None):
        self.params = params
        super(CustomDatePicker, self).__init__(attrs=attrs)

    class Media:
        css = {
            'all': (staticfiles_storage.url(
                'js/jquery-ui.min.css'),)
        }
        js = (
            STATIC_URL + 'js/jquery.js',
            STATIC_URL + 'js/jquery-ui.min.js',
        )
