from django.shortcuts import redirect

def login_check(function):
    def wrap(request,*args,**kwargs):
        user=request.session.get('user')
        if user is None or not user:
            return redirect('/') #로그인페이지로 redirect
        return function(request,*args,**kwargs)
    return wrap