from django.db import models
from common.models import BaseModel

class Type(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table= 'type'

    def __str__(self):
        return self.name
