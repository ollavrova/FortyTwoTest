from django.core.management.base import BaseCommand
from django.db.models.loading import get_models


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        for model in get_models():
            out = "{0}: {1}".format(model.__name__, model.objects.count())
            self.stdout.write(out)
            self.stderr.write("error: {0}".format(out))
