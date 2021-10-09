from django.shortcuts import render,redirect
from .decorators import login_check
from django.contrib.auth.hashers import make_password, check_password
from .models import User
# Create your views here.

def home(request):
    if request.session.get('user'):
        return redirect('/label')
    else:
        return redirect('/login')

def logout(request):
    if request.session.get('user'):
        del request.session['user']
    return redirect('/')

def login(request):
    if request.method=='POST':
        login_id=request.POST.get('id',None)
        login_pw=request.POST.get('pw',None)

        res_data={}
        if not (login_id and login_pw):
            res_data['error']="* Incorrect ID or password."
        else:
            try:
                user=User.objects.get(user_id=login_id)
            except User.DoesNotExist:
                res_data['error']="* Incorrect ID or password."
                return render(request, 'login.html',res_data)

            if not check_password(login_pw,user.password):
                res_data['error']="* Incorrect ID or password."
            else:
                request.session['user']=login_id
                return redirect('/')

        return render(request, 'login.html',res_data) #error을 담은 res_data를 login.html 에게 넘겨줌


    else:
        return render(request,'login.html')

def join(request):
    if request.method=="POST":
        join_id=request.POST.get('id',None)
        join_pw=request.POST.get('pw',None)
        join_pwcheck=request.POST.get('pwcheck',None)

        res_data={}

        if not (join_id and join_pw and join_pwcheck):
            res_data['error']='* Fill out the form.'
        elif len(join_id)<8 or len(join_id)>20:
            res_data['error']='* Please enter ID of 8 to 20 characters.'
        elif len(join_pw)<8 or len(join_pw)>20:
            res_data['error']='* Please enter password of 8 to 20 characters.'
        elif join_pw !=join_pwcheck:
            res_data['error']='* Passwords do not match.'
        else:
            try:
                user=User.objects.get(user_id=join_id)
                res_data['error']='* ID already exists.'
            except:
                new_user=User(
                    user_id=join_id,
                    password=make_password(join_pw)
                )
                new_user.save()
                return redirect('/')
        return render(request,'join.html',res_data)
    else:
        return render(request,'join.html')

@login_check
def setting(request):
    return render(request,'setting.html')