from django.db.models import Sum
from django.db.models.functions import ExtractYear
from rest_framework.views import APIView
from rest_framework.response import Response
from filereader.models import RepositoryLanguage


class LanguageStatsView(APIView):
    """
    API для получения статистики по языкам
    """

    def get(self, request):

        stats = (
            RepositoryLanguage.objects
            .annotate(year=ExtractYear("repository__created_at"))
            .values("year", "name")
            .annotate(total_size=Sum("size"))
            .order_by("year", "-total_size")
        )

        result = {}

        for item in stats:
            year = item["year"]
            language = item["name"]
            size = item["total_size"]

            result.setdefault(year, [])

            if len(result[year]) < 5:
                result[year].append({
                    "language": language,
                    "total_size": size
                })

        return Response(result)
