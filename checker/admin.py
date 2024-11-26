from django.contrib import admin

from checker.models import ScrapedData, Partner


class AdminPartner(admin.ModelAdmin):
    list_display = ['name', 'web_site', 'logo']
    list_filter = ['name']


class AdminScrapedData(admin.ModelAdmin):
    list_display = ['partner']
    list_filter = ['last_update']


admin.site.register(Partner, AdminPartner)
admin.site.register(ScrapedData, AdminScrapedData)
