import json
from django.core.management.base import BaseCommand
from filereader.models import Repository
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = "Добавление данных в базу через bulk create пачками по 1000"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        repositories = []

        for repo in data:
            repositories.append(
                Repository(
                    owner=repo.get("owner"),
                    name=repo.get("name"),
                    stars=repo.get("stars", 0),
                    forks=repo.get("forks", 0),
                    primary_language=repo.get("primaryLanguage"),
                    created_at=parse_datetime(repo.get("createdAt")),
                )
            )

        Repository.objects.bulk_create(repositories, batch_size=1000) # добавляем через bulk для оптимизации

        self.stdout.write(
            self.style.SUCCESS(f"Imported {len(repositories)} repositories")
        )