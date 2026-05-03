from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from accounts.models import User, Profile
from ...models import Objective


class Command(BaseCommand):

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.fake = Faker()

    def handle(self, *args, **options):
        for _ in range(5):
            user = User.objects.create_user(
                username=self.fake.user_name(),
                password="test@123456",
            )
            print(user.username)
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.country = self.fake.country()
            profile.phone = self.fake.phone_number()
            profile.save()

            for _ in range(choice([3, 6, 9])):
                objective = Objective.objects.create(
                    owner=user,
                    title=self.fake.paragraph(nb_sentences=1),
                    description=self.fake.paragraph(nb_sentences=3),
                    status=choice([True, False]),
                )
