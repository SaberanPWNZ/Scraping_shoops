from django.urls import path

from checker.views import PartnersScrapingInfo

urlpatterns = [
    path('scraped/', PartnersScrapingInfo.as_view(), name='scraped'),
]
