from django.db import models
from common.models import BaseModel
from users.models import User


class Status(BaseModel):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'status'
        unique_together = ['name', 'user']
