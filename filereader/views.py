import json
from django.db.models import Count
from django.db.models.functions import ExtractYear
from rest_framework.views import APIView
from rest_framework.response import Response
from filereader.models import Repository


class LanguageStatsView(APIView):
    """
    API дляполучения информации по языкам програмирования
    Возвращает топ 5 по годам
    """

    def get(self, request):

        stats = (
            Repository.objects
            .exclude(primary_language__isnull=True)
            .exclude(primary_language="")
            .annotate(year=ExtractYear("created_at"))
            .values("year", "primary_language")
            .annotate(count=Count("id"))
            .order_by("year", "-count")
        )

        result = {}

        for item in stats:
            year = item["year"]
            language = item["primary_language"]
            count = item["count"]

            result.setdefault(year, [])

            if len(result[year]) < 5:
                result[year].append({
                    "language": language,
                    "count": count
                })
        
        return Response(result)