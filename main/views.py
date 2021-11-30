from django.http.response import Http404, JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.decorators import login_check
from .models import Image
from login.models import User,Label
from django.core.files.base import ContentFile, File
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime
from django.core import serializers
import json
from PIL import Image as Image1
 
from .models import Model
import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchsummary import summary
from torch import optim
from torch.optim.lr_scheduler import StepLR

# dataset and transformation
from torchvision import datasets
import torchvision
import torchvision.transforms as transforms
from torchvision import models
from torch.utils.data import DataLoader, Dataset
import os
import cv2
from glob import glob

# display images
from torchvision import utils
import matplotlib.pyplot as plt

# utils
import numpy as np
import time
import copy

from django.conf import settings


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Create your views here.

class userDataset(Dataset):
    def __init__(self, file_list, label_list, transforms_data=None):
        self.file_list = file_list
        self.label_list=label_list
        self.transforms = transforms_data
    
    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        name=self.file_list[idx].split('/')[-1]

        #방법1
        #stream=open((settings.MEDIA_ROOT+"\\image\\"+name).encode('utf-8'),'rb')
        #bytes=bytearray(stream.read())
        #numpyArray=np.asarray(bytes,dtype=np.uint8)
        #img=cv2.imdecode(numpyArray,cv2.IMREAD_UNCHANGED)
        #img = cv2.imread(self.file_list[idx])


        img = cv2.imdecode(np.fromfile(settings.MEDIA_ROOT+"\\image\\"+name, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        im_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image1.fromarray(im_rgb)
#        label = self.label_list[idx]
        label = torch.tensor(self.label_list[idx])
        img_transformed = self.transforms(img)


        #img = Image1.open(settings.MEDIA_ROOT+"\\image\\"+name)
        
        #if self.transforms is not None:
        #    img = self.transforms(img)

        return (img_transformed,label,name)


def dataSet(label1_image, label2_image) :
    image_list = label1_image|label2_image
    
    data_list = []
    Label_list = []
        
    
    for image in image_list:
        data_list.append(image.image.url)
        Label_list.append(image.labeling_int)


        transforms_data =  transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            #normalize,
        ])

    train_ds = userDataset(file_list = data_list, label_list = Label_list,transforms_data=transforms_data)
    train_loader = DataLoader(train_ds, batch_size = 8, shuffle=True)

    return train_ds, train_loader

def modelTrain(train_loader, train_ds, userID) :
    save_path=settings.MEDIA_URL+'model/'
    model = models.resnet18(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 1)
    model = model.to(device)
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    summary(model, (3, 224, 224), device=device.type)

    num_epochs = 30
    model.train()
    start_time = time.time()

    accList = []
    modelList = []

    print(device)

    # 전체 반복(epoch) 수 만큼 반복하며
    for epoch in range(num_epochs):
        running_loss = 0.
        running_corrects = 0

        # 배치 단위로 학습 데이터 불러오기
        for inputs, labels,name in train_loader:
            print(inputs,labels)
            print(name)
            inputs = inputs.to(device)
            labels = labels.to(device)

            # 모델에 입력(forward)하고 결과 계산
            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

            # 역전파를 통해 기울기(gradient) 계산 및 학습 진행
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
            try:
                image=Image.objects.get(image_name=name)
                image.training=True
                image.predict=preds
                image.save()
            except:
                pass

        epoch_loss = running_loss / len(train_ds)
        epoch_acc = running_corrects / len(train_ds) * 100.
        accList.append(epoch_acc) # 정확도가 90%을 넘기지 못할 시, 가장 좋은 정확도의 모델을 위해 사용
        modelList.append(model)
        # 학습 과정 중에 결과 출력
        print('#{} Loss: {:.4f} Acc: {:.4f}% Time: {:.4f}s'.format(epoch, epoch_loss, epoch_acc, time.time() - start_time))

        # 정확도가 90%를 넘겼을 시, 그 모델을 바로 사용
        if epoch_acc >= 90:
            torch.save(model, save_path + userID + '.pt') # database path입력하기
            dat=open(save_path + userID + '.pt',mode='r')
            new_model=Model()
            new_model.model=File(dat)
            new_model.model_name=userID+".pt"
            

            new_model.save()

    # 정확도가 90%을 넘지 않을 경우, 30번 중 정확도가 가장 높은 모델 저장
    idx = accList.index(max(accList))
    torch.save(modelList[idx], save_path) # database path 입력하기

    #model save 수정 필요



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
        label1_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label1).order_by('upload_date')
        label2_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label2).order_by('upload_date')
        unlabeled_images=Image.objects.filter(user=user,labeling=False).order_by('upload_date') #upload날짜 오름차순
    else:    
        label1_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label1).order_by('-upload_date')
        label2_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label2).order_by('-upload_date')
        unlabeled_images=Image.objects.filter(user=user,labeling=False).order_by('-upload_date') #upload날짜 내림차순

    total=len(label1_images)+len(label2_images)+len(unlabeled_images)

    return render(request,'label.html',{'userid':user_id,'total':total ,'label1':label.label1,'label2':label.label2,'label1_images':label1_images,'label2_images':label2_images,'unlabeled_images':unlabeled_images})

@login_check
def train(request):
    if request.method=='GET':
        a=request.GET.get('sort',None)

        user_id=request.session.get('user')
        try:
            user = User.objects.get(user_id=user_id)
            images=Image.objects.filter(user=user,labeling=True,training=True)
            label=Label.objects.get(user=user.id)
        except:
            return render(request,'train.html',{'userid':user_id})

        images=images.order_by('-upload_date')
        label1_images=images.filter(labeling_int=0).order_by('-upload_date')
        label2_images=images.filter(labeling_int=1).order_by('-upload_date')

        #개수
        total=len(images)
        label1_len=len(label1_images)
        label2_len=len(label2_images)

        label1_correct=len(label1_images.filter(predict="0"))
        label2_correct=len(label2_images.filter(predict="1"))
        total_correct=label1_correct+label2_correct 

        if a=='ascending':
            images=images.order_by('upload_date')
            label1_images=label1_images.order_by('upload_date')
            label2_images=label2_images.order_by('upload_date')
        elif a=='correct':
            print("im here")
            label1_images=label1_images.filter(predict="0")
            label2_images=label2_images.filter(predict="1")

            images=label1_images|label2_images
        elif a=='incorrect':
            label1_images=label1_images.filter(predict="1")
            label2_images=label2_images.filter(predict="0")

            images=label1_images|label2_images

        return render(request,'train.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,
        'all':images,'total_len':total,'total_correct':total_correct,
        'label1_images':label1_images,'label1_len':label1_len,'label1_correct':label1_correct,
        'label2_images':label2_images,'label2_len':label2_len,'label2_correct':label2_correct})

    elif request.method =='POST':
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
        train_loader, train_ds = dataSet(label1_image, label2_image)

        trainModel = modelTrain(train_loader, train_ds,user.user_id)
        label1_json=serializers.serialize('json',label1_image)
        label2_json=serializers.serialize('json',label2_image)
        
        return JsonResponse({"label1":label1_json,"label2":label2_json},status=200)


@login_check
def predict_image(request):
    user_id=request.session.get('user')
    try:
        user = User.objects.get(user_id=user_id)
        images=Image.objects.filter(user=user,labeling=True,training=True)
    except:
        return render(request,'predict_Images.html',{'userid':user_id})

    label1_images=images.filter(labeling_int=0)
    label2_images=images.filter(labeling_int=1)

    #개수
    total=len(images)
    label1_len=len(label1_images)
    label2_len=len(label2_images)

    label1_correct=len(label1_images.filter(predict="0"))
    label2_correct=len(label2_images.filter(predict="1"))
    total_correct=label1_correct+label2_correct 

    return render(request,'predict_Images.html',{'userid':user_id,'total_len':total,'total_correct':total_correct,
    'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct})

@csrf_exempt
@login_check
def predict_camera(request):
    if request.method=='GET':
        user_id=request.session.get('user')

        try:
            user = User.objects.get(user_id=user_id)
            images=Image.objects.filter(user=user,labeling=True,training=True)
        except:
            return render(request,'predict_Images.html',{'userid':user_id})

        label1_images=images.filter(labeling_int=0)
        label2_images=images.filter(labeling_int=1)

        #개수
        total=len(images)
        label1_len=len(label1_images)
        label2_len=len(label2_images)

        label1_correct=len(label1_images.filter(predict="0"))
        label2_correct=len(label2_images.filter(predict="1"))
        total_correct=label1_correct+label2_correct

        return render(request,'predict_Camera.html',{'userid':user_id,'total_len':total,'total_correct':total_correct,
    'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct})
    elif request.method=='POST':
        user_id=request.session.get('user')

        return HttpResponse("Banana",status=200)        

@login_check
def predict_export(request):
    user_id=request.session.get('user')
    try:
        user = User.objects.get(user_id=user_id)
        images=Image.objects.filter(user=user,labeling=True,training=True)
    except:
        return render(request,'predict_Images.html',{'userid':user_id})

    label1_images=images.filter(labeling_int=0)
    label2_images=images.filter(labeling_int=1)

    #개수
    total=len(images)
    label1_len=len(label1_images)
    label2_len=len(label2_images)

    label1_correct=len(label1_images.filter(predict="0"))
    label2_correct=len(label2_images.filter(predict="1"))
    total_correct=label1_correct+label2_correct

    return render(request,'predict_Export.html',{'userid':user_id,'total_len':total,'total_correct':total_correct,
    'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct})


@csrf_exempt
def image(request):
    if(request.method=='POST'):
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        time=datetime.now()
        img_data=base64.b64decode(img_string)
        #이미지 이름
        key=user_id+time.strftime("%Y%m%d%H%M%S")+".png" 

        try:
            user=User.objects.get(user_id=user_id)
        except:
            return Http404("error")

        #db에 저장
        image=Image()
        image.user=user
        #image.user_id=user_id
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

        try:
            user=User.objects.get(user_id=user_id)
        except:
            return Http404("error")

        image=Image()
        image.user=user
        #image.user_id=user_id
        image.image_name=img.name
        image.image=img
        image.save()
        return redirect("/")
    else:
        return HttpResponse("hello image")


@csrf_exempt
def delete(request):
    if(request.method=='POST'):
        user_id=request.session.get('user')
        img_name=request.POST.get('image_name')
        #image delete
        try:
            user=User.objects.get(user_id=user_id)
            Image.objects.get(user=user,image_name=img_name).delete()
        except:
            pass
        return redirect("/")


@csrf_exempt
def update(request):
    if request.method=='POST':
        img_name=request.POST.get('image_name')
        label=request.POST.getlist('label',None)[0]
        user_id=request.session.get('user')
        try:
            user=User.objects.get(user_id=user_id)
            label_ob=Label.objects.get(user=user)
        except:
            return redirect("/")

        image=Image.objects.get(image_name=img_name)
        image.labeling=True
        if label==label_ob.label1:
            image.labeling_name=label
            image.labeling_int=0
        elif label==label_ob.label2:
            image.labeling_name=label
            image.labeling_int=1
        else:
            redirect("/")

        #model update
        image.save()
        return redirect("/")



