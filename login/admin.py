from django.contrib import admin
from .models import User,Label

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=('user_id','registered_dttm',)

class LabelAdmin(admin.ModelAdmin):
    list_display=('user','label1','label2')
admin.site.register(User,UserAdmin)
admin.site.register(Label,LabelAdmin)