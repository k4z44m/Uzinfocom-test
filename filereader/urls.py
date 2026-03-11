from django.urls import path
from .views import LanguageStatsView

urlpatterns = [
    path("languages/", LanguageStatsView.as_view()),
]
