from django.urls import path
from . import views

urlpatterns=[
    path('cam/',views.cam),
    path('save/',views.image)
]