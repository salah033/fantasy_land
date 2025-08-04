from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Suppliers
from .resources import SupplierResource

@admin.register(Suppliers)
class SupplierAdmin(ImportExportModelAdmin) :
    resource_class = SupplierResource
