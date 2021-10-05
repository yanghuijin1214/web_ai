from django.contrib import admin
from django.utils.html import format_html
from .models import Image

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" />'.format(obj.image.url))

    list_display=('userid','upload_date','image_tag','labeling','labeling_name')
    
    image_tag.exmpty_value_display="Not available"

admin.site.register(Image,ImageAdmin)