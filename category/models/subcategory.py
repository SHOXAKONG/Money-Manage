from django.db import models
from category.models.category import Category
from common.models import BaseModel

class Subcategory(BaseModel):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'subcategory'