from django.core.management.base import BaseCommand
from Users.models import CustomUser

class Command(BaseCommand):
    help = 'Create 10 test users for the application'

    def handle(self, *args, **kwargs):
        test_users = [
            {'username': "Giorgi Giorgobiani", 'email': "giorgi.giorgobiani@example.com"},
            {'username': "Nino Beridze", 'email': "nino.beridze@example.com"},
            {'username': "Lasha Kapanadze", 'email': "lasha.kapanadze@example.com"},
            {'username': "Tamar Gelashvili", 'email': "tamar.gelashvili@example.com"},
            {'username': "Irakli Tsiklauri", 'email': "irakli.tsiklauri@example.com"},
            {'username': "Mariam Kalandadze", 'email': "mariam.kalandadze@example.com"},
            {'username': "Saba Chikhladze", 'email': "saba.chikhladze@example.com"},
            {'username': "Ana Mchedlishvili", 'email': "ana.mchedlishvili@example.com"},
            {'username': "Davit Kharabadze", 'email': "davit.kharabadze@example.com"},
            {'username': "Salome Japaridze", 'email': "salome.japaridze@example.com"},
        ]

        shared_password = 'Ragaca123'
        created_users = []

        for user_data in test_users:
            name_parts = user_data['username'].split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ''

            if CustomUser.objects.filter(username=user_data['username']).exists():
                self.stdout.write(self.style.WARNING(f"User {user_data['username']} already exists. Skipping..."))
                continue

            user = CustomUser.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=first_name,
                last_name=last_name,
                password=shared_password,
                is_active=True,
                is_staff=False,
            )

            created_users.append(user)
            self.stdout.write(self.style.SUCCESS(f"User {user.username} created successfully."))

        self.stdout.write(self.style.SUCCESS(f"Created {len(created_users)} test users."))

