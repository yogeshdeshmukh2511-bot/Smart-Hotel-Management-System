import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or update hotel manager user"

    def handle(self, *args, **kwargs):

        username = os.environ.get("MANAGER_USERNAME")
        password = os.environ.get("MANAGER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                self.style.ERROR(
                    "MANAGER_USERNAME or MANAGER_PASSWORD is not set."
                )
            )
            return

        User = get_user_model()

        user, created = User.objects.get_or_create(
            username=username
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Manager user '{username}' created successfully."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Manager user '{username}' updated successfully."
                )
            )