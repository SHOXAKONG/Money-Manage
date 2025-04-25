from django.db import models
from common.models import BaseModel

class Status(BaseModel):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'status'

