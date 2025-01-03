from django.contrib import admin

from checker.models import Partner
from items.models import Brand


class AdminPartner(admin.ModelAdmin):
    list_display = ['name', 'web_site', 'logo']
    list_filter = ['name']




class AdminBrand(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Partner, AdminPartner)
admin.site.register(Brand, AdminBrand)
