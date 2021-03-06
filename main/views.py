from django.http.response import Http404, JsonResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from login.decorators import login_check
from .models import Image,Model
from login.models import User,Label
from django.core.files.base import ContentFile, File
from django.views.decorators.csrf import csrf_exempt
import base64
from datetime import datetime
from django.utils import timezone
from django.core import serializers
import json
from django.core.files import File as DjangoFile
from PIL import Image as Image1
 
import torch.optim as optim
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchsummary import summary
from torch import optim
from torch.optim.lr_scheduler import StepLR

# dataset and transformation
from torchvision import datasets
import torchvision.transforms as transforms
from torchvision import models
from torch.utils.data import DataLoader, Dataset
import os
from glob import glob


# utils
import numpy as np
import time
import io

from django.conf import settings


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Create your views here.

class userDataset(Dataset):
    def __init__(self, file_list, label_list):
        self.file_list = file_list
        self.label_list = label_list
        self.transforms = transforms.Compose([
                transforms.Resize((224,224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
                #normalize,
            ])

    def __len__(self):
        return len(self.file_list)

    def __getitem__(self, idx):
        name = self.file_list[idx].split('/')[-1]
        img=Image1.open(settings.MEDIA_ROOT+"\\image\\"+name).convert('RGB')
        img_transformed = self.transforms(img)
        label = self.label_list[idx]

        return img_transformed,label,name


def modelTrain(label1_image, label2_image, userID) :
    image_list = label1_image|label2_image
    try:
        user=User.objects.get(user_id=userID)
    except:
        return
        
    data_list = []
    Label_list = []

    for image in image_list:
        data_list.append(image.image.url)
        Label_list.append(float(image.labeling_int))

    train_ds = userDataset(file_list = data_list, label_list = Label_list)
    train_loader = DataLoader(train_ds, batch_size = 8, shuffle=True)

    save_path=settings.MEDIA_ROOT+"\\model\\"
    model = models.resnet18(pretrained=True)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 1)
    model = model.to(device)
    criterion=torch.nn.BCEWithLogitsLoss(pos_weight=torch.tensor(5.))
    #criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    
    summary(model, (3, 224, 224), device=device.type)
    

    num_epochs = 30
    model.train()
    start_time = time.time()

    accList = []
    modelList = []
    timeList=[]

    # ?????? ??????(epoch) ??? ?????? ????????????
    for epoch in range(num_epochs):
        running_loss = 0.
        running_corrects = 0
        corrected=0

        # ?????? ????????? ?????? ????????? ????????????
        for inputs, labels, name in train_loader:

            inputs = inputs.to(device)
            labels = labels.to(device) 
            labels = labels.unsqueeze(1)

            # ????????? ??????(forward)?????? ?????? ??????
            optimizer.zero_grad()

            outputs = model(inputs)

            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs.float(), labels.float())
            
            # ???????????? ?????? ?????????(gradient) ?????? ??? ?????? ??????
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            
            running_corrects += torch.sum(preds == labels.data)

            for i in range(len(name)):
                try:
                    image=Image.objects.get(image_name=name[i])
                    image.training=True
                    if outputs.detach().numpy()[i]<0:
                        image.predict=0
                    else:
                        image.predict=1
                    image.save()
                    if image.predict==image.labeling_int:
                        corrected+=1
                except:
                    #print("i'm here!")
                    return

        epoch_loss = running_loss / len(train_ds)
        corrected_acc=corrected/len(train_ds)*100.
        #epoch_acc = running_corrects / len(train_ds) * 100.
        
        learning_time=time.time() - start_time #???????????? DB??? ?????????????????? ????????? ??????
        
        accList.append(corrected_acc) # ???????????? 90%??? ????????? ?????? ???, ?????? ?????? ???????????? ????????? ?????? ??????
        modelList.append(model)
        timeList.append(learning_time)
        # ?????? ?????? ?????? ?????? ??????
        print('#{} Loss: {:.4f} Acc: {:.4f}% Time: {:.4f}s'.format(epoch, epoch_loss, corrected_acc, learning_time))

        if corrected_acc >= 90:
            torch.save( model,'media/model/'+userID + '__.pt') # database path????????????
            file_obj1 = DjangoFile(open(save_path + userID + '__.pt', mode='rb'), name=userID+".pt")

            try:
                new_model=Model.objects.get(user=user,model_name=userID+'.pt')
                new_model.model=file_obj1
                new_model.data_size=len(image_list)
                new_model.accuracy=corrected_acc
                new_model.learning_time=learning_time
                new_model.created_date=timezone.now()
            except: #????????? ?????? ?????? ??????
                new_model=Model()
                new_model.user=user
                new_model.model=file_obj1
                new_model.model_name=userID+".pt"
                new_model.data_size=len(image_list)
                new_model.accuracy=corrected_acc
                new_model.learning_time=learning_time

            new_model.save()
            return

    # ???????????? 90%??? ?????? ?????? ??????, 30??? ??? ???????????? ?????? ?????? ?????? ??????
    idx = accList.index(max(accList))

    #???????????
    torch.save( modelList[idx],'media/model/'+userID + '__.pt') # database path????????????
    file_obj1 = DjangoFile(open(save_path + userID + '__.pt', mode='rb'), name=userID+".pt")            
    new_model=Model()
    new_model.user=user
    new_model.model=file_obj1
    new_model.model_name=userID+".pt"
    new_model.data_size=len(image_list)
    new_model.accuracy=accList[idx]
    new_model.learning_time=timeList[idx]
    new_model.save()



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
    #???????????? ????????????
    if a=='ascending':
        label1_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label1).order_by('upload_date')
        label2_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label2).order_by('upload_date')
        unlabeled_images=Image.objects.filter(user=user,labeling=False).order_by('upload_date') #upload?????? ????????????
    else:    
        label1_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label1).order_by('-upload_date')
        label2_images=Image.objects.filter(user=user,labeling=True,labeling_name=label.label2).order_by('-upload_date')
        unlabeled_images=Image.objects.filter(user=user,labeling=False).order_by('-upload_date') #upload?????? ????????????
    
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
        
        try:
            model=Model.objects.get(user=user)
        except:
            model=None
        
        images=images.order_by('-upload_date')
        label1_images=images.filter(labeling_int=0).order_by('-upload_date')
        label2_images=images.filter(labeling_int=1).order_by('-upload_date')

        #??????
        total=len(images)
        print(total)
        label1_len=len(label1_images)
        label2_len=len(label2_images)

        if model==None:
            return render(request,'train.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,'train':'no'})
        

        train_time=round(float(model.learning_time),4)
        

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
        
        return render(request,'train.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,'train':'yes','time':train_time,
        'all':images,'total_len':total,'total_correct':total_correct,
        'label1_images':label1_images,'label1_len':label1_len,'label1_correct':label1_correct,
        'label2_images':label2_images,'label2_len':label2_len,'label2_correct':label2_correct})

    elif request.method =='POST':
        user_id=request.POST.get('userid')
        print(user_id)
        try:
            user = User.objects.get(user_id=user_id)
            label=Label.objects.get(user=user.id)
        except:
            return HttpResponse("Error",status=400)
        label1_image=Image.objects.filter(user=user,labeling_name=label.label1)
        label2_image=Image.objects.filter(user=user,labeling_name=label.label2)
        
        trainModel = modelTrain(label1_image, label2_image,user.user_id)
        label1_json=serializers.serialize('json',label1_image)
        label2_json=serializers.serialize('json',label2_image)
        
        return JsonResponse({"label1":label1_json,"label2":label2_json},status=200)


def get_prediction(image,user_id):
    save_path=settings.MEDIA_ROOT+"\\model\\"
            
    model = torch.load(save_path + user_id + '.pt')

    model.eval()
    transforms_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = transforms_test(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        print(preds[0])
        if outputs.detach().numpy()[0]<0:
            predict=0
        else:
            predict=1

    return predict


@csrf_exempt
@login_check
def predict_image(request):
    if request.method=='GET':
        user_id=request.session.get('user')
        try:
            user = User.objects.get(user_id=user_id)
            images=Image.objects.filter(user=user,labeling=True,training=True)
            label=Label.objects.get(user=user.id)
        except:
            return render(request,'predict_Images.html',{'userid':user_id})
        try:
            model=Model.objects.get(user=user)
        except:
            model=None            
        label1_images=images.filter(labeling_int=0)
        label2_images=images.filter(labeling_int=1)

        if model==None:
            return render(request,'predict_Images.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,'train':'no'})

        train_time=round(float(model.learning_time),4)
        #??????
        total=len(images)
        label1_len=len(label1_images)
        label2_len=len(label2_images)

        label1_correct=len(label1_images.filter(predict="0"))
        label2_correct=len(label2_images.filter(predict="1"))
        total_correct=label1_correct+label2_correct 

        return render(request,'predict_Images.html',{'userid':user_id,'total_len':total,'total_correct':total_correct, 'label1':label.label1,'label2':label.label2,'train':'yes','time':train_time,
        'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct})
    elif request.method=='POST':
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        user_id2=request.session.get('user')
        if user_id==user_id2:
            try:
                user=User.objects.get(user_id=user_id)
                model=Model.objects.get(user=user)
                label=Label.objects.get(user=user.id)
            except:
                return HttpResponse("Error",status=200)
            try:
                img_data=base64.b64decode(img_string)
                bytesIo=io.BytesIO(img_data)
                image=Image1.open(bytesIo)
            except:
                return HttpResponse("Error",status=200)
            
            pred=get_prediction(image,user_id)
            if pred==0:
                predict=label.label1
            else:
                predict=label.label2

            return HttpResponse(predict,status=200)

        return HttpResponse("Error",status=200)


@csrf_exempt
@login_check
def predict_camera(request):
    if request.method=='GET':
        user_id=request.session.get('user')

        try:
            user = User.objects.get(user_id=user_id)
            images=Image.objects.filter(user=user,labeling=True,training=True)
            label=Label.objects.get(user=user.id)
        except:
            return render(request,'predict_Camera.html',{'userid':user_id})

        try:
            model=Model.objects.get(user=user)
        except:
            model=None

        if model==None:
            return render(request,'predict_Camera.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,'train':'no'})

        label1_images=images.filter(labeling_int=0)
        label2_images=images.filter(labeling_int=1)

        train_time=round(float(model.learning_time),4)
        #??????
        total=len(images)
        label1_len=len(label1_images)
        label2_len=len(label2_images)

        label1_correct=len(label1_images.filter(predict="0"))
        label2_correct=len(label2_images.filter(predict="1"))
        total_correct=label1_correct+label2_correct

        return render(request,'predict_Camera.html',{'userid':user_id,'total_len':total,'total_correct':total_correct,'label1':label.label1,'label2':label.label2,'train':'yes','time':train_time,
    'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct})
    elif request.method=='POST':
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        user_id2=request.session.get('user')
        if user_id==user_id2:
            try:
                user=User.objects.get(user_id=user_id)
                model=Model.objects.get(user=user)
                label=Label.objects.get(user=user.id)
            except:
                return HttpResponse("Error",status=200)

            try:
                img_data=base64.b64decode(img_string)
                bytesIo=io.BytesIO(img_data)
                image=Image1.open(bytesIo).convert('RGB')
            except:
                return HttpResponse("Error",status=200)
            
            pred=get_prediction(image,user_id)
            if pred==0:
                predict=label.label1
            else:
                predict=label.label2
            print(predict)            
            return HttpResponse(predict,status=200)
        return HttpResponse("Error",status=200)        

@login_check
def predict_export(request):
    user_id=request.session.get('user')
    try:
        user = User.objects.get(user_id=user_id)
        images=Image.objects.filter(user=user,labeling=True,training=True)
        label=Label.objects.get(user=user.id)
    except:
        return render(request,'predict_Export.html',{'userid':user_id})
    try:
        model=Model.objects.get(user=user)
    except:
        model=None
    
    if model==None:
        return render(request,'predict_Export.html',{'userid':user_id,'label1':label.label1,'label2':label.label2,'train':'no'})

    
    label1_images=images.filter(labeling_int=0)
    label2_images=images.filter(labeling_int=1)

    train_time=round(float(model.learning_time),4)
    
    #??????
    total=len(images)
    label1_len=len(label1_images)
    label2_len=len(label2_images)
    label1_correct=len(label1_images.filter(predict="0"))
    label2_correct=len(label2_images.filter(predict="1"))
    total_correct=label1_correct+label2_correct

    return render(request,'predict_Export.html',{'userid':user_id,'total_len':total,'total_correct':total_correct,'label1':label.label1,'label2':label.label2,'train':'yes','time':train_time,
    'label1_len':label1_len,'label1_correct':label1_correct,'label2_len':label2_len,'label2_correct':label2_correct,'model':model.model})


@csrf_exempt
@login_check
def image(request):
    if(request.method=='POST'):
        img_string=request.POST.get('image',None)
        user_id=request.POST.get('userid',None)
        time=datetime.now()
        img_data=base64.b64decode(img_string)
        #????????? ??????
        key=user_id+time.strftime("%Y%m%d%H%M%S")+".png" 

        try:
            user=User.objects.get(user_id=user_id)
        except:
            return Http404("error")

        #db??? ??????
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
@login_check
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
@login_check
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
@login_check
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


@csrf_exempt
@login_check
def delete_model(request):
    if request.method=='POST':
        user_id1=request.POST.get('userid')
        user_id2=request.session.get('user')
        if user_id1==user_id2:
            try:
                user=User.objects.get(user_id=user_id2)
                Model.objects.get(user=user).delete()
                Image.objects.filter(user=user).delete()
            except:
                raise Http404("error")
        
        return redirect("/")
