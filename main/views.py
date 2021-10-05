from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Image
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime

# Create your views here.
def cam(request):
    user_id=request.session.get('user')
    return render(request,'cam.html',{'userid':user_id})

def label(request):
    user_id=request.session.get('user')
    images=Image.objects.filter(userid=user_id).order_by('-upload_date') #upload날짜 내림차순
    print(images)
    for image in images:
        print(image.image.url)
    return render(request,'label.html',{'userid':user_id,'images':images})

def train(request):
    user_id=request.session.get('user')
    return render(request,'train.html',{'userid':user_id})

def predict_image(request):
    user_id=request.session.get('user')
    return render(request,'predict_Images.html',{'userid':user_id})

def predict_camera(request):
    user_id=request.session.get('user')
    return render(request,'predict_Camera.html',{'userid':user_id})

def predict_export(request):
    user_id=request.session.get('user')
    return render(request,'predict_Export.html',{'userid':user_id})

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
        image.image_name=key
        image.image.save(key,ContentFile(img_data),save=True)
        image.save()

        return HttpResponse("hello")
    else:
        return HttpResponse("hello image")