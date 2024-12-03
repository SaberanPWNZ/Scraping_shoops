from django.urls import path
from checker.views import DataTableView, PartnerTableView

urlpatterns = [
    path('data/', DataTableView.as_view(), name='data_table'),
    path('data/<slug:slug>/', PartnerTableView.as_view(), name='partner_table'),
]
