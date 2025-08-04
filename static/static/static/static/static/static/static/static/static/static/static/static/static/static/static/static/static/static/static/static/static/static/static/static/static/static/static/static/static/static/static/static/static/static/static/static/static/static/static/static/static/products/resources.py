from import_export import resources
from .models import Products, Categories


class ProductResource(resources.ModelResource):
    class Meta:
        model = Products

class CategorieResource(resources.ModelResource):
    class Meta:
        model = Categories