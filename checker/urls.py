
from django.urls import path
from .views import ComparingDataKtc, PartnerDataView

urlpatterns = [
    path('all-partners/', ComparingDataKtc.as_view(), name='scraped-data'),
    path('partners/<slug:slug>/', PartnerDataView.as_view(), name='partner_data')
]
