from django.db import models

# Create your models here.
class User(models.Model):
    user_id=models.CharField(max_length=64)
    password=models.CharField(max_length=64)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name="등록시간")

    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user'