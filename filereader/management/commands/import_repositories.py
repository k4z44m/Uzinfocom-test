import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from filereader.models import Repository, RepositoryLanguage


class Command(BaseCommand):
    help = "Импорт репозиториев и языков из JSON через bulk_create"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        repositories = []
        languages = []

        for repo in data:
            repositories.append(
                Repository(
                    owner=repo.get("owner"),
                    name=repo.get("name"),
                    stars=repo.get("stars", 0),
                    forks=repo.get("forks", 0),
                    created_at=parse_datetime(repo.get("createdAt")),
                )
            )

        Repository.objects.bulk_create(repositories, batch_size=1000)

        for repo_obj, repo in zip(repositories, data):

            for lang in repo.get("languages", []):
                languages.append(
                    RepositoryLanguage(
                        repository=repo_obj,
                        name=lang.get("name"),
                        size=lang.get("size", 0),
                    )
                )

        RepositoryLanguage.objects.bulk_create(languages, batch_size=1000)

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(repositories)} repositories and {len(languages)} languages"
            )
        )