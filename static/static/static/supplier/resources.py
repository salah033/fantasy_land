from import_export import resources
from .models import Suppliers


class SupplierResource(resources.ModelResource):
    class Meta:
        model = Suppliers