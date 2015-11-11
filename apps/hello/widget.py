from django.contrib.staticfiles.storage import staticfiles_storage
from django.forms import DateInput
from django.utils.safestring import mark_safe
from fortytwo_test_task.settings import STATIC_URL


class CustomDatePicker(DateInput):
    def __init__(self, params='', attrs=None):
        self.params = params
        super(CustomDatePicker, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        rendered = super(CustomDatePicker, self).render(name, value,
                                                        attrs=attrs)
        return rendered + mark_safe(u'''<script type="text/javascript">
            $('#id_%s').datepicker({%s});
            </script>''' % (name, self.params,))

    class Media:
        css = {
            'all': (staticfiles_storage.url('jquery-ui-1.11.2.custom/jquery-ui.min.css'),)
        }
        js = (
            STATIC_URL + 'jquery-ui-1.11.2.custom/external/jquery/jquery.js',
            STATIC_URL + 'jquery-ui-1.11.2.custom/jquery-ui.min.js',
        )
