import pandas as pd
import os.path
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
import logging


class Command(BaseCommand):
    help = "Creating users accounts"

    full_path = 'travels/management/files/users.xlsx'
    users = pd.read_excel(full_path)

    def handle(self, *args, **options):
        for i in range(len(self.users)):
            #_, created = User.objects.get_or_create(self.users["Username"][i], self.users["Email"][i], self.users["Password"][i])
            created = get_user_model().objects.create_user(self.users["Username"][i], self.users["Email"][i], self.users["Password"][i])
            created.save()
            # if created:
            #     logging.info("Dodano użytkownika ", self.users["Username"][i])
