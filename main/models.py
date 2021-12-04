from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.html import format_html
import os
from login.models import User

# Create your models here.

class Image(models.Model):
    user=models.ForeignKey(User,verbose_name="user",on_delete=models.CASCADE)
    #user_id=models.CharField(max_length=32,verbose_name="사용자 아이디")
    upload_date=models.DateTimeField(auto_now_add=True,verbose_name="업로드시간")
    image_name=models.CharField(max_length=50,verbose_name="이미지명")
    image=models.ImageField(upload_to="image/",verbose_name="image")
    labeling=models.BooleanField(default=False,verbose_name="라벨링 여부")
    labeling_name=models.CharField(max_length=50,verbose_name="라벨링명",null=True)
    labeling_int=models.IntegerField(default=-1,verbose_name="라벨링 숫자") # -1 : unlabeled , 0 : label 1 , 1 : label2
    training=models.BooleanField(default=False,verbose_name="학습 여부") 
    predict=models.CharField(max_length=50,verbose_name="예측결과",default="",null=True)

    def __str__(self):
        return self.image_name

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Image, self).delete(*args, **kargs)
    
#    def image_tag(self,obj):
#        return format_html('<img src="%s" />'.format(obj.image.url))

#    image_tag.short_description = 'Image'
#    image_tag.allow_tags = True    
class OverWriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT,name))
        return name
class Model(models.Model):
    user=models.ForeignKey(User,verbose_name="User",on_delete=models.CASCADE)
    model_name=models.CharField(max_length=50,verbose_name="모델 파일 이름")
    model=models.FileField(upload_to="model/",storage=OverWriteStorage,verbose_name="파일 경로")
    created_date=models.DateTimeField(auto_now_add=True,verbose_name="파일 생성 시간")
    data_size=models.IntegerField()
    accuracy=models.CharField(max_length=10,verbose_name="정확도")
    learning_time=models.CharField(max_length=10)

    def __str__(self):
        return self.model_name

    def delete(self, *args, **kargs):
        if self.model:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.model.path))
        super(Model, self).delete(*args, **kargs)