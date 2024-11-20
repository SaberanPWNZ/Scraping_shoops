
from django.urls import path
from .views import ComparingDataKtc, PartnerDataView

urlpatterns = [
    path('all-partners/', ComparingDataKtc.as_view(), name='scraped-data'),
    path('partner/<str:partner_name>/', PartnerDataView.as_view(), name='partner_data')
]
