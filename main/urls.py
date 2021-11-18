from django.urls import path
from . import views

urlpatterns=[
    path('cam/',views.cam),
    path('save/',views.image),
    path('upload/',views.upload),
    path('delete/',views.delete),
    path('update/',views.update)
]