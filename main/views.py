from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.decorators import login_check
from .models import Image
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime


# Create your views here.

@login_check
def cam(request):
    user_id=request.session.get('user')
    return render(request,'cam.html',{'userid':user_id})


@login_check
def label(request):
    user_id=request.session.get('user')
    images=Image.objects.filter(userid=user_id).order_by('-upload_date') #upload날짜 내림차순

    return render(request,'label.html',{'userid':user_id,'images':images})

@login_check
def train(request):
    user_id=request.session.get('user')
    return render(request,'train.html',{'userid':user_id})


@login_check
def predict_image(request):
    user_id=request.session.get('user')
    return render(request,'predict_Images.html',{'userid':user_id})

@login_check
def predict_camera(request):
    user_id=request.session.get('user')
    return render(request,'predict_Camera.html',{'userid':user_id})

@login_check
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

@csrf_exempt
def upload(request):
    if(request.method=='POST'):
        img=request.FILES['file']
        user_id=request.session.get('user')
        aa=img.name.split(".")
        time=datetime.now()
        img.name=user_id+time.strftime("%Y%m%d%H%M%S")+"."+aa[1]
        image=Image()
        image.userid=user_id
        image.image_name=img.name
        image.image=img
        image.save()
        return redirect("/")
    else:
        return HttpResponse("hello image")