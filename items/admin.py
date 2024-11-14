from django.contrib import admin
from .models import Item, Status, Warranty, Category


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'article', 'status', 'partner_price', 'rrp_price', 'warranty', 'ean', 'category')
    search_fields = ('title', 'article')
    list_filter = ('status', 'category')
    list_per_page = 20


class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    search_help_text = ['статус товару']
    list_filter = ['name']


class WarrantyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    search_help_text = ['гарантія']
    list_filter = ['name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    search_help_text = ['категорія']
    list_filter = ['name']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Status, StatusAdmin)
from django.contrib import admin

# Register your models here.
