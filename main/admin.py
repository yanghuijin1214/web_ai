from django.contrib import admin
from django.utils.html import format_html
from .models import Image,Model

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    list_display=('user_id','upload_date','image_tag','labeling','labeling_name','labeling_int')
    
    image_tag.exmpty_value_display="Not available"

class ModelAdmin(admin.ModelAdmin):
    #def image_tag(self, obj):
    #    return format_html('<file src="{}" />'.format(obj.model.url))

    list_display=('user','model_name','model','created_date','data_size','accuracy','learning_time')
    
    #image_tag.exmpty_value_display="Not available"
admin.site.register(Image,ImageAdmin)
admin.site.register(Model,ModelAdmin)