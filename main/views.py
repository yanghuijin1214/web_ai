from django.http.response import JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.decorators import login_check
from .models import Image
from login.models import User,Label
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime
from django.core import serializers
import json


# Create your views here.



@login_check
def cam(request):
    user_id=request.session.get('user')
    return render(request,'cam.html',{'userid':user_id})


@login_check
def label(request):
    a=request.GET.get('sort',None)
    
    user_id=request.session.get('user')
    try:
        user = User.objects.get(user_id=user_id)
        label=Label.objects.get(user=user.id)
    except:
        return render(request,'label.html')
    #이미지들 가져오기
    if a=='ascending':
        label1_images=Image.objects.filter(user_id=user_id,labeling=True,labeling_name=label.label1).order_by('upload_date')
        label2_images=Image.objects.filter(user_id=user_id,labeling=True,labeling_name=label.label2).order_by('upload_date')
        unlabeled_images=Image.objects.filter(user_id=user_id,labeling=False).order_by('upload_date') #upload날짜 오름차순
    else:    
        label1_images=Image.objects.filter(user_id=user_id,labeling=True,labeling_name=label.label1).order_by('-upload_date')
        label2_images=Image.objects.filter(user_id=user_id,labeling=True,labeling_name=label.label2).order_by('-upload_date')
        unlabeled_images=Image.objects.filter(user_id=user_id,labeling=False).order_by('-upload_date') #upload날짜 내림차순

    total=len(label1_images)+len(label2_images)+len(unlabeled_images)

    return render(request,'label.html',{'userid':user_id,'total':total ,'label1':label.label1,'label2':label.label2,'label1_images':label1_images,'label2_images':label2_images,'unlabeled_images':unlabeled_images})

@login_check
def train(request):
    if request.method=='GET':
        user_id=request.session.get('user')
        return render(request,'train.html',{'userid':user_id})
    elif request.method=='POST':
        #body=json.loads(request.body.decode('utf-8'))
        user_id=request.POST.get('userid')
        print(user_id)
        try:
            user = User.objects.get(user_id=user_id)
            label=Label.objects.get(user=user.id)
        except:
            return HttpResponse("Error",status=400)
        label1_image=Image.objects.filter(user_id=user_id,labeling_name=label.label1)
        label2_image=Image.objects.filter(user_id=user_id,labeling_name=label.label2)
        model_train(user_id,label1_image,label2_image)
        label1_json=serializers.serialize('json',label1_image)
        label2_json=serializers.serialize('json',label2_image)
        
        return JsonResponse({"label1":label1_json,"label2":label2_json},status=200)

def model_train(user_id,label1_image,label2_image):
    print("user_id : ",user_id)
    print("label1")
    for image in label1_image:
        print("user_id : ",image.user_id)
        print("image_name : ",image.image_name)
        print("image path : " ,image.image.url)
        print("labeling_name :",image.labeling_name)
    print("==================")
    print("label2")
    for image in label2_image:
        print("user_id : ",image.user_id)
        print("image_name : ",image.image_name)
        print("image path : " ,image.image.url)
        print("labeling_name :",image.labeling_name)    

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
    if(request.method=='POST'):
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        time=datetime.now()
        img_data=base64.b64decode(img_string)
        #이미지 이름
        key=user_id+time.strftime("%Y%m%d%H%M%S")+".png" 

        #db에 저장
        image=Image()
        image.user_id=user_id
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
        image.user_id=user_id
        image.image_name=img.name
        image.image=img
        image.save()
        return redirect("/")
    else:
        return HttpResponse("hello image")


@csrf_exempt
def delete(request):
    if(request.method=='POST'):
        img_name=request.POST.get('image_name')
        #image delete
        Image.objects.get(image_name=img_name).delete()
        return redirect("/")


@csrf_exempt
def update(request):
    if request.method=='POST':
        img_name=request.POST.get('image_name')
        label=request.POST.getlist('label',None)[0]
        
        #model update
        image=Image.objects.get(image_name=img_name)
        image.labeling=True;image.labeling_name=label
        image.save()
        return redirect("/")



