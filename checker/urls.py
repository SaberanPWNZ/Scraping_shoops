
from django.urls import path
from .views import ScrapedDataView

urlpatterns = [
    path('scraped-data/', ScrapedDataView.as_view(), name='scraped-data'),
]
