from common.models import BaseModel
from django.db import models
from users.models import User


class Type(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'user']
        db_table = 'type'

    def __str__(self):
        return self.name
