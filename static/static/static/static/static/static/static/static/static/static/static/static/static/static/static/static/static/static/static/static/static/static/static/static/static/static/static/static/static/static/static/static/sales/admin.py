from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Sale, SaleItem
from .resources import SaleResource, SaleItemResource



@admin.register(Sale)
class SaleAdmin(ImportExportModelAdmin) :
    resource_class = SaleResource

@admin.register(SaleItem)
class SaleItemAdmin(ImportExportModelAdmin) :
    resource_class = SaleItemResource
