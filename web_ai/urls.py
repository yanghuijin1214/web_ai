"""web_ai URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from main.views import cam,image,label,train,predict_image,
from main.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('cam/',cam),
    path('label/',label),
    path('train/',train),
    path('predict/image/',predict_image),
    path('predict/camera/',predict_camera),
    path('predict/export/',predict_export),
    path('image/',include('main.urls'))
]
