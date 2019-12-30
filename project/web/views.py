from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms

#主页
def index(request):
    return render(request, 'index.html')

#登录
def login(request):
    if request.session.get('is_login',None):
        return redirect('/index')
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', {"message":message})
    return render(request, 'login.html')

#注册
def register(request):
    message = ""
    if request.session.get('is_login',None):
        return redirect('/index')
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'register.html', {"message":message})
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', {"message":message})
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', {"message":message})
                models.User.objects.create(name = username, password = password1, email = email)
                return redirect('/login')
    return render(request, 'register.html', {"message":message})

#注销
def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index")
    request.session.flush()
    return redirect("/index")

#用户页
def user(request):
    if not request.session.get('is_login',None):
        return redirect('/index')
    return render(request, 'user.html')

#总作品页
def works(request):
    return render(request, 'works.html')

#作品编写页
def write_work(request):
    if not request.session.get('is_login',None):
        return redirect('/index')
    if request.method == "POST":
        work_form = forms.WorkForm(request.POST)
        if work_form.is_valid():
            name = work_form.cleaned_data["workname"]
            date = work_form.cleaned_data["date"]
            carrier = work_form.cleaned_data["carrier"]
            introduction = work_form.cleaned_data["introduction"]
            models.Work.objects.create(name = name, date = date, carrier = carrier, introduction = introduction)
            work = models.Work.objects.get(name = name, date = date, carrier = carrier)
            return redirect('/works/'+str(work.pk))
    return render(request, 'write_work.html')

#作品页
def work(request,id):
    work = models.Work.objects.get(pk = int(id))
    return render(request, 'work.html', {"name":work.name, "date":work.date, "carrier":work.carrier, "introduction":work.introduction})
