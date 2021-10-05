from django.db import models
from django.utils.html import format_html


# Create your models here.

class Image(models.Model):
    userid=models.CharField(max_length=64,verbose_name="사용자 아이디")
    upload_date=models.DateTimeField(auto_now_add=True,verbose_name="업로드시간")
    image_name=models.CharField(max_length=100,verbose_name="이미지명")
    image=models.ImageField(upload_to="image/",verbose_name="image")
    labeling=models.BooleanField(default=False,verbose_name="라벨링 여부")
    labeling_name=models.CharField(max_length=100,verbose_name="라벨링명")

    def __str__(self):
        return self.image_name
    
#    def image_tag(self,obj):
#        return format_html('<img src="%s" />'.format(obj.image.url))

#    image_tag.short_description = 'Image'
#    image_tag.allow_tags = True    