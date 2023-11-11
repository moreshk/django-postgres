from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import uuid

class Command(BaseCommand):
    help = 'Generates referral codes for users who do not have one yet'

    def handle(self, *args, **options):
        User = get_user_model()
        users_without_referral_code = User.objects.filter(referral_code__isnull=True)
        for user in users_without_referral_code:
            user.referral_code = str(uuid.uuid4())[:8]
            user.save()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated referral codes for {users_without_referral_code.count()} users'))