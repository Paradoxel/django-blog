from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Category, Tag
import os
import random
from django.conf import settings
from django.core.files import File


class Command(BaseCommand):
    help = "Generate professional fake blog posts"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of posts to generate",
        )

        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all posts before generating new ones",
        )

    CATEGORY_POOL = [
        "Django", "Python", "Backend",
        "APIs", "Databases", "Testing", "DevOps"
    ]

    TAG_POOL = [
        "django", "python", "rest",
        "sql", "security", "performance", "testing"
    ]

    STATUS_DISTRIBUTION = [
        (Post.Status.PUBLISHED, 0.7),
        (Post.Status.DRAFT, 0.2),
        (Post.Status.ARCHIVED, 0.1),
    ]

    def handle(self, *args, **options):
        fake = Faker()
        User = get_user_model()

        count = options["count"]

        # -----------------------
        # RESET OPTION
        # -----------------------
        if options["reset"]:
            Post.objects.all().delete()
            self.stdout.write(self.style.WARNING("All posts deleted."))

        # -----------------------
        # USER
        # -----------------------
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                email="test@gmail.com",
                password="12345678"
            )

        # -----------------------
        # DATA POOLS
        # -----------------------
        categories = [
            Category.objects.get_or_create(name=name)[0]
            for name in self.CATEGORY_POOL
        ]

        tags = [
            Tag.objects.get_or_create(name=name)[0]
            for name in self.TAG_POOL
        ]

        # -----------------------
        # IMAGES (YOUR NEW SET)
        # -----------------------
        image_folder = os.path.join(settings.BASE_DIR, "static", "img")
        images = [
            "b1.jpg", "b2.jpg", "b3.jpg",
            "d1.jpg", "d2.jpg", "d3.jpg"
        ]

        # -----------------------
        # HELPERS
        # -----------------------
        def weighted_status():
            r = random.random()
            cumulative = 0
            for status, weight in self.STATUS_DISTRIBUTION:
                cumulative += weight
                if r <= cumulative:
                    return status
            return Post.Status.PUBLISHED

        # -----------------------
        # GENERATION LOOP
        # -----------------------
        for i in range(count):
            image_name = random.choice(images)
            image_path = os.path.join(image_folder, image_name)

            with open(image_path, "rb") as img:
                post = Post.objects.create(
                    author=user,
                    title=fake.sentence(nb_words=6),
                    content=fake.paragraph(nb_sentences=12),
                    excerpt=fake.sentence(nb_words=18),
                    image=File(img, name=image_name),
                    primary_tag=random.choice(tags),
                    view_count=random.randint(0, 20000),
                    status=weighted_status(),
                )

            post.categories.add(
                *random.sample(categories, k=random.randint(1, 3))
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} professional fake posts generated successfully!"
            )
        )