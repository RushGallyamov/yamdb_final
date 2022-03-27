import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = "Loads category entities to db from csv file"

    supported_entities = {
        "category": Category,
        "genre": Genre,
        "titles": Title,
        "genre_title": Title.genre.through,
        "users": User,
        "review": Review,
        "comments": Comment,
    }

    def add_arguments(self, parser):
        parser.add_argument("entity_name", nargs="+", type=str)

    def handle(self, *args, **options):
        if options["entity_name"] == ["all"]:
            entities_to_load = list(self.supported_entities.keys())
            self.stdout.write(f"Loading entities: {entities_to_load}.")
            options["entity_name"] = entities_to_load

        for entity_name in options["entity_name"]:
            self.stdout.write("")
            self.stdout.write(f'Loading entity "{entity_name}"...')

            if entity_name not in self.supported_entities:
                error_msg = (
                    f'Error: Entity "{entity_name}" is not supported!'
                    f" Supported entities are "
                    f"{list(self.supported_entities.keys())}"
                )
                self.stdout.write(self.style.ERROR(error_msg))
                continue

            model = self.supported_entities[entity_name]
            file_path = f"{settings.STATICFILES_DIRS[0]}data/{entity_name}.csv"

            with open(file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row = self._fill_row_with_related_entities(row, model)
                    if row:
                        model.objects.update_or_create(**row)

            self.stdout.write(
                self.style.SUCCESS(f'Loaded entity "{entity_name}".')
            )

        if len(options["entity_name"]) > 1:
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("All entities are loaded!"))

    @staticmethod
    def _process_title_row(row):
        category_id = row["category"]
        category = Category.objects.get(id=category_id)
        if not category:
            return None

        row["category"] = category

        return row

    @staticmethod
    def _process_review_row(row):
        title_id = row["title_id"]
        title = Title.objects.get(id=title_id)
        if not title:
            return None

        row["title"] = title

        author_id = row["author"]
        author = User.objects.get(id=author_id)
        if not author:
            return None

        row["author"] = author

        return row

    @staticmethod
    def _process_comment_row(row):
        review_id = row["review_id"]
        review = Review.objects.get(id=review_id)
        if not review:
            return None

        row["review"] = review

        author_id = row["author"]
        author = User.objects.get(id=author_id)
        if not author:
            return None

        row["author"] = author

        return row

    def _fill_row_with_related_entities(self, row, model):
        if model == Title:
            return self._process_title_row(row)
        if model == Review:
            return self._process_review_row(row)
        if model == Comment:
            return self._process_comment_row(row)

        return row
