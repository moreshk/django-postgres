from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError

class Command(createsuperuser.Command):
    help = 'Create a superuser with just an email and password.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument('--password', dest='password', default=None, help='Specifies the password for the superuser.')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')

        if not email or not password:
            raise CommandError('Both --email and --password options must be provided.')

        try:
            self.UserModel._default_manager.create_superuser(email=email, password=password)
            self.stdout.write("Superuser created successfully.")
        except Exception as e:
            raise CommandError(e)
