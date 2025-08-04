from import_export import resources
from .models import Sale, SaleItem


class SaleResource(resources.ModelResource):
    class Meta:
        model = Sale

class SaleItemResource(resources.ModelResource):
    class Meta:
        model = SaleItem