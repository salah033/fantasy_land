from import_export import resources
from .models import UserNote, UserShopOrder, UserCustomer, UserCustomerOrder

class UserNoteResource(resources.ModelResource) : 
    class Meta: 
        model = UserNote

class UserShopOrderResource(resources.ModelResource) : 
    class Meta: 
        model = UserShopOrder

class UserCustomerResource(resources.ModelResource) : 
    class Meta: 
        model = UserCustomer

class UserCustomerOrderResource(resources.ModelResource) : 
    class Meta: 
        model = UserCustomerOrder