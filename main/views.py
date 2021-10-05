from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Image
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime

# Create your views here.
def cam(request):
    return render(request,'cam.html')

def label(request):
    return render(request,'label.html')

def train(request):
    return render(request,'train.html')

def predict_image(request):
    return render(request,'predict_Images.html')

def predict_camera(request):
    return render(request,'predict_Camera.html')

def predict_export(request):
    return render(request,'predict_Export.html')

@csrf_exempt
def image(request):
    print("image capture")

    if(request.method=='POST'):
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        time=datetime.now()
        img_data=base64.b64decode(img_string)
        #이미지 이름
        key=user_id+time.strftime("%Y%m%d%H%M%S")+".png" 

        #db에 저장
        image=Image()
        image.userid=user_id
        image.image.save(key,ContentFile(img_data),save=True)
        image.save()

        return HttpResponse("hello")
    else:
        return HttpResponse("hello image")