from django.db import models

# Create your models here.
class User(models.Model):
    user_id=models.CharField(max_length=32)
    password=models.CharField(max_length=64)
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name="등록시간")
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'user'

class Label(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    label1=models.CharField(max_length=50,default="Label 1",verbose_name="라벨링1 이름")
    label2=models.CharField(max_length=50,default="Label 2",verbose_name="라벨링2 이름")

    def __str__(self):
        return self.user

    class Meta:
        db_table = 'Label'