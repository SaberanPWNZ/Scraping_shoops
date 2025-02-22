from django.urls import path

from checker.views import PartnersScrapingInfo, PartnerItemSearch

urlpatterns = [
    path('scraped/', PartnersScrapingInfo.as_view(), name='scraped'),
    # path('search', PartnerItemSearch.as_view(), name='search'),
    path('search/<str:query>/', PartnerItemSearch.as_view(), name='search_with_query'),
]
