from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Products, Categories
from .resources import ProductResource, CategorieResource
from django.utils.html import format_html

@admin.register(Products)
class ProductAdmin(ImportExportModelAdmin) :
    resource_class = ProductResource
    
    def image_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="60"/>', obj.photo.url)
        return "No Image"
    
    image_tag.short_description = 'Preview'

    def is_low_stock(self, obj):
        return obj.quantity <= 5
    is_low_stock.boolean = True  
    is_low_stock.short_description = 'is Low Stock'

    actions = ['mark_as_inactive']
    def mark_as_inactive(self, request, queryset):
        queryset.update(active=False)
        self.message_user(request, "Marked as inactive.")
    
    search_fields = ['name']
    list_filter = ['category', 'active']
    list_display = ['image_tag', 'name', 'quantity', 'category__name', 'price', 'purchase_date', 'active', 'is_low_stock']
    list_editable = ['price', 'active']
    list_display_links = ['name']
    fieldsets = (
    ('Basic Info', {
        'fields': ('name','bare_code', 'reference', 'category')
    }),
    ('Pricing & Stock', {
        'fields': ('price', 'quantity', 'supplier', 'active', 'purchase_date')
    }),
    ('Other Info', {
        'fields': ('designation', 'photo')
    })
                )
    list_per_page = 20

@admin.register(Categories)
class CategorieAdmin(ImportExportModelAdmin) :
    resource_class = CategorieResource


