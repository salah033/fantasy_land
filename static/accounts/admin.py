from django.contrib import admin
from .models import UserNote, UserShopOrder, UserCustomer, UserCustomerOrder
from .resources import UserNoteResource, UserShopOrderResource, UserCustomerResource, UserCustomerOrderResource
from import_export.admin import ImportExportModelAdmin


@admin.register(UserNote)
class UserNoteAdmin(ImportExportModelAdmin) :
    resource_class = UserNoteResource

    readonly_fields = ['type', 'employee']

@admin.register(UserShopOrder)
class UserShopOrderAdmin(ImportExportModelAdmin) : 
    resource_class = UserShopOrderResource

    readonly_fields = ['type', 'employee']

@admin.register(UserCustomer)
class UserCustomerAdmin(ImportExportModelAdmin) : 
    resource_class = UserCustomerResource

    readonly_fields = ['type', 'employee']

@admin.register(UserCustomerOrder)
class UserCustomerOrderAdmin(ImportExportModelAdmin) :
    resource_class = UserCustomerOrderResource

    readonly_fields = ['type', 'employee']

# Register your models here.
