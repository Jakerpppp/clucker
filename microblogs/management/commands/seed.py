from django.core.management.base import BaseCommand, CommandError
from faker import Faker

from microblogs.models import User

class Command(BaseCommand):
    def __init__(self):
        super.__init__()
        self.faker = Faker("en_GB")


    def handle(self, *args, **options):
        """ for i in range(20):
            user = User.objects.create_user(
                username = "@" + self.faker.name(),
                first_name = self.faker.name(),
                last_name = self.faker.lastName();
            ) """
        pass
        