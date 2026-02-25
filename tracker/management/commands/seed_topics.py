"""
Management command to seed Firestore with all DNN topics.
Usage: python manage.py seed_topics
"""
from django.core.management.base import BaseCommand
from tracker.topics_data import DNN_TOPICS
from tracker.firebase import get_db, seed_topics


class Command(BaseCommand):
    help = "Seed Firestore dnn_topics collection with all DNN topics and subtopics."

    def handle(self, *args, **options):
        db = get_db()
        if not db:
            self.stderr.write(self.style.ERROR("Firebase not configured. Set FIREBASE_CREDENTIALS."))
            return
        try:
            n = seed_topics(DNN_TOPICS)
            self.stdout.write(self.style.SUCCESS(f"Seeded {n} topics to Firestore."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(str(e)))
