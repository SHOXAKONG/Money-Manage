from django.db import models

from category.models.type import Type
from common.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name
