from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Make an existing user a superuser'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        try:
            user = User.objects.get(username=username)
            user.is_staff     = True
            user.is_superuser = True
            user.save()
            self.stdout.write(f'Successfully made {username} a superuser')
        except User.DoesNotExist:
            self.stdout.write(f'User {username} does not exist')