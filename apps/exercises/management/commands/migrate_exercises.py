import os

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from apps.exercises.models import Exercise


class Command(BaseCommand):
    help = "Migrate exercise media to MinIO storage"

    def handle(self, *args, **options):
        self.migrate_media()

    def migrate_media(self):
        BATCH_SIZE = 50

        exercises = Exercise.objects.exclude(media_url__isnull=True).exclude(
            media_url__exact=""
        )
        total = exercises.count()
        self.stdout.write(f"Found {total} exercises with media.")

        for batch_start in range(0, total, BATCH_SIZE):
            batch = exercises[batch_start : batch_start + BATCH_SIZE]
            for exercise in batch:
                try:
                    old_url = exercise.media_url
                    response = requests.get(old_url, timeout=10)
                    response.raise_for_status()

                    filename = self.generate_filename(exercise.name, old_url)
                    self.stdout.write(filename)
                    new_path = f"exercises/{filename}"

                    # Save file via Django Storage backend (MinIO)
                    if not default_storage.exists(new_path):
                        default_storage.save(new_path, ContentFile(response.content))

                    # Update exercise.media_url to new stable path
                    new_url = default_storage.url(new_path)
                    exercise.media_url = new_url
                    exercise.save(update_fields=["media_url"])

                    self.stdout.write(f"✅ Migrated: {exercise.name}")
                except Exception as e:
                    self.stderr.write(f"❌ Failed to migrate {exercise.name}: {e}")

    def generate_filename(self, name: str, url: str) -> str:
        """Generate clean filename based on exercise name and file extension."""
        name_part = name.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")
        ext = os.path.splitext(url)[1] or ".jpg"
        return f"{name_part}{ext}"
