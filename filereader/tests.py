from django.test import TestCase
from rest_framework.test import APIClient
from filereader.models import Repository
from datetime import datetime


class LanguageStatsTest(TestCase):

    def test_languages_endpoint(self):
        client = APIClient()

        Repository.objects.create(
            owner="test",
            name="repo1",
            primary_language="Python",
            created_at=datetime(2020, 1, 1),
            stars=10,
            forks=1
        )

        response = client.get("/api/languages/")

        self.assertEqual(response.status_code, 200)