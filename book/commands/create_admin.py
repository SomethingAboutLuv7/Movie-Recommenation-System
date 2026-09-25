from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser non-interactively if one does not exist'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created.'))
            else:
                self.stdout.write('Superuser already exists, skipping.')
        else:
            self.stdout.write('DJANGO_SUPERUSER_USERNAME/PASSWORD not set, skipping.')