from django.contrib import admin

from checker.models import ScrapedData, Partner
from items.models import Brand


class AdminPartner(admin.ModelAdmin):
    list_display = ['name', 'web_site', 'logo']
    list_filter = ['name']


class AdminScrapedData(admin.ModelAdmin):
    list_display = ['partner']
    list_filter = ['last_update']


class AdminBrand(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Partner, AdminPartner)
admin.site.register(ScrapedData, AdminScrapedData)
admin.site.register(Brand, AdminBrand)
