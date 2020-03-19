from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Avg
from django.db.models import Count
from . import models
from . import forms
import random

#主页
def home(request):
    new_list = list(models.Work.objects.all())
    all_work = random.sample(new_list,10 if len(new_list) > 10 else len(new_list))
    work_list = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        work_list.append(new_entry)

    new_list = list(models.Post.objects.filter(tag = "disscussion"))
    all_disscussion = random.sample(new_list,5 if len(new_list) > 5 else len(new_list))
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        disscussion_list.append(new_entry)

    new_list = list(models.Post.objects.filter(tag = "question"))
    all_question = random.sample(new_list,5 if len(new_list) > 5 else len(new_list))
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        question_list.append(new_entry)

    example = {"work_list":work_list, "disscussion_list":disscussion_list, "question_list":question_list}
    return render(request, 'home.html', {"example":example})

#登录
def signin(request):
    if request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        signin_form = forms.SigninForm(request.POST)
        message = "请检查填写的内容！"
        if signin_form.is_valid():
            username = signin_form.cleaned_data['username']
            password = signin_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/home')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'signin.html', {"message":message})
    return render(request, 'signin.html')

#注册
def login(request):
    message = ""
    if request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password1 = login_form.cleaned_data['password1']
            password2 = login_form.cleaned_data['password2']
            email = login_form.cleaned_data['email']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'login.html', {"message":message})
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login.html', {"message":message})
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login.html', {"message":message})
                models.User.objects.create(name = username, password = password1, email = email)
                return redirect('/signin')
    return render(request, 'login.html', {"message":message})

#注销
def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/home")
    request.session.flush()
    return redirect("/home")

#用户页
def user(request):
    if not request.session.get('is_login',None):
        return redirect('/home')

    all_work = models.Collection.objects.filter(tag = "work_collection", uid = request.session.get('user_id',None))
    work_list = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.wpid
        new_entry["name"] = models.Work.objects.get(id = entry.wpid).name
        work_list.append(new_entry)

    all_disscussion = models.Collection.objects.filter(tag = "disscussion_collection", uid = request.session.get('user_id',None))
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.wpid
        new_entry["name"] = models.Post.objects.get(id = entry.wpid).name
        disscussion_list.append(new_entry)

    all_question = models.Collection.objects.filter(tag = "question_collection", uid = request.session.get('user_id',None))
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.wpid
        new_entry["name"] = models.Post.objects.get(id = entry.wpid).name
        question_list.append(new_entry)

    collection = {"work_list":work_list, "disscussion_list":disscussion_list, "question_list":question_list}
    return render(request, 'user.html', {"collection":collection})

#作品总页
def works(request,tag):
    work_list = []
    if tag == "none":
        all_work = models.Work.objects.all()
    else:
        list_1 = models.Work.objects.all()
        list_2 = models.Tag.objects.filter(name = tag)
        for entry in list_1:
            new_entry = {}
            new_entry["id"] = entry.id
            new_entry["name"] = entry.name
            if list_2.filter(wid = entry.id).exists():
                work_list.append(new_entry)
        all_work = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        work_list.append(new_entry)

    tag_list = []
    all_tag = models.Tag.objects.all().values("name").distinct()
    for entry in all_tag:
        new_entry = {}
        new_entry["name"] = entry["name"]
        tag_list.append(new_entry)
    return render(request, 'works.html', {"work_list":work_list, "tag_list":tag_list})

#作品推荐编写页
def write_work(request):
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        work_form = forms.WorkForm(request.POST)
        if work_form.is_valid():
            name = work_form.cleaned_data["name"]
            date = work_form.cleaned_data["date"]
            introduction = work_form.cleaned_data["introduction"]
            work = models.Work.objects.create(name = name, date = date, introduction = introduction)
            return redirect('/work/detail/'+str(work.pk))
    return render(request, 'write_work.html')

#作品页
def work(request,id):
    db_work = models.Work.objects.get(pk = id)
    work = {}
    work["id"] = db_work.id
    work["name"] = db_work.name
    work["date"] = db_work.date
    work["introduction"] = db_work.introduction

    if request.method == "POST" and request.session.get('is_login',None):
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                models.Comment.objects.create(tag = "work_comment", wpid = db_work.id, uid = request.session.get('user_id',None), content = content, delete = False)
        if "score_update" in request.POST:
            score_form = forms.ScoreForm(request.POST)
            if score_form.is_valid():
                score = score_form.cleaned_data["score"]
                try:
                    new_score = models.Score.objects.get(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分")
                    new_score.score = score
                    new_score.save()
                except:
                    models.Score.objects.create(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分", score = score, main = False)
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "work_collection", wpid = db_work.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "work_collection", wpid = db_work.id, uid = request.session.get('user_id',None))
        if "tag_update" in request.POST:
            tag_form = forms.TagForm(request.POST)
            if tag_form.is_valid():
                tag_name = tag_form.cleaned_data["tag_name"]
                try:
                    models.Tag.objects.get(wid = db_work.id, uid = request.session.get('user_id',None))
                except:
                    models.Tag.objects.create(wid = db_work.id, uid = request.session.get('user_id',None), name = tag_name, main = False)
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            print(delete_form.is_valid())
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_coment = models.Comment.objects.get(id = delete_id)
                delete_coment.delete = True
                delete_coment.save()

    comment_list = []
    all_comment = models.Comment.objects.filter(tag = "work_comment", wpid = db_work.id, delete = False)
    for entry in all_comment:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["user_id"] = entry.uid
        new_entry["user_name"] = models.User.objects.get(id = entry.uid).name
        new_entry["content"] = entry.content
        new_entry["date"] = entry.date
        comment_list.append(new_entry)

    score = {}
    try:
        score["avg_s"] = models.Score.objects.filter(wid = db_work.id, name = "总分").aggregate(avg_s=Avg("score"))["avg_s"]
    except:
        score["avg_s"] = False
    try:
        score["user_s"] = models.Score.objects.get(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分").score
    except:
        score["user_s"] = False

    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "work_collection", wpid = db_work.id, uid = request.session.get('user_id',None))
            collection = "collection_button_1"
        except:
            collection = "collection_button_2"

    tag_list = []
    all_tag = models.Tag.objects.filter(wid = db_work.id).values('name').annotate(count_n=Count("name"))
    choose_work_id = {}
    for entry in all_tag:
        new_entry = {}
        new_entry["name"] = entry["name"]
        new_entry["count"] = entry["count_n"]
        tag_list.append(new_entry)
        choose_tag = models.Tag.objects.filter(name = entry["name"]).values('wid').distinct()
        for entry_2 in choose_tag:
            if entry_2["wid"] != db_work.id:
                if entry_2["wid"] not in choose_work_id.keys():
                    choose_work_id[entry_2["wid"]] = 1
                else:
                    choose_work_id[entry_2["wid"]] = choose_work_id[entry_2["wid"]] + 1
    tag = {"unwritten":True, "tag_list":tag_list}
    try:
        models.Tag.objects.get(wid = db_work.id, uid = request.session.get('user_id',None))
        tag["unwritten"] = False
    except:
        tag["unwritten"] = True

    choose_work_id = sorted(choose_work_id.items(), key = lambda kv:kv[1])
    choose_work_list = []
    counter = 0
    for entry in choose_work_id:
        if counter >= 5:
            break
        new_entry = {}
        new_entry["id"] = entry[0]
        new_entry["name"] = models.Work.objects.get(id = entry[0]).name
        choose_work_list.append(new_entry)
        counter = counter + 1
    return render(request, 'work.html', {"work":work, "comment_list":comment_list, "score":score, "collection":collection, "tag":tag, "choose_work_list":choose_work_list})

#讨论总页
def disscussions(request):
    all_disscussion = models.Post.objects.filter(tag = "disscussion")
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        disscussion_list.append(new_entry)
    return render(request, 'disscussions.html', {"disscussion_list":disscussion_list})

#讨论编写页
def write_disscussion(request):
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            name = post_form.cleaned_data["name"]
            content = post_form.cleaned_data["content"]
            post = models.Post.objects.create(tag ="disscussion", uid = request.session.get('user_id',None), name = name, content = content, delete = False)
            return redirect('/disscussion/'+str(post.pk))
    return render(request, 'write_disscussion.html')

#讨论页
def disscussion(request,id):
    db_disscussion = models.Post.objects.get(pk = id)
    disscussion = {}
    disscussion["id"] = db_disscussion.id
    disscussion["name"] = db_disscussion.name
    disscussion["content"] = db_disscussion.content
    disscussion["user_name"] =  models.User.objects.get(id = db_disscussion.uid).name
    disscussion["date"] = db_disscussion.date

    if request.method == "POST" and request.session.get('is_login',None):
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                models.Comment.objects.create(tag = "disscussion_comment", wpid = db_disscussion.id, uid = request.session.get('user_id',None), content = content, delete = False)
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "disscussion_collection", wpid = db_disscussion.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "disscussion_collection", wpid = db_disscussion.id, uid = request.session.get('user_id',None))
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            print(delete_form.is_valid())
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_coment = models.Comment.objects.get(id = delete_id)
                delete_coment.delete = True
                delete_coment.save()

    comment_list = []
    all_comment = models.Comment.objects.filter(tag = "disscussion_comment", wpid = db_disscussion.id, delete = False)
    for entry in all_comment:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["user_id"] = entry.uid
        new_entry["user_name"] = models.User.objects.get(id = entry.uid).name
        new_entry["content"] = entry.content
        new_entry["date"] = entry.date
        comment_list.append(new_entry)


    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "disscussion_collection", wpid = db_disscussion.id, uid = request.session.get('user_id',None))
            collection = "collection_button_1"
        except:
            collection = "collection_button_2"
    return render(request, 'disscussion.html', {"disscussion":disscussion, "comment_list":comment_list, "collection":collection})

#问题总页
def questions(request):
    all_question = models.Post.objects.filter(tag = "question")
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        question_list.append(new_entry)
    return render(request, 'questions.html', {"question_list":question_list})

#问题编写页
def write_question(request):
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            name = post_form.cleaned_data["name"]
            content = post_form.cleaned_data["content"]
            post = models.Post.objects.create(tag ="question", uid = request.session.get('user_id',None), name = name, content = content, delete = False)
            return redirect('/question/'+str(post.pk))
    return render(request, 'write_question.html')

#问题页
def question(request,id):
    db_question = models.Post.objects.get(pk = id)
    question = {}
    question["id"] = db_question.id
    question["name"] = db_question.name
    question["content"] = db_question.content
    question["user_name"] =  models.User.objects.get(id = db_question.uid).name
    question["date"] = db_question.date

    if request.method == "POST" and request.session.get('is_login',None):
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                models.Comment.objects.create(tag = "question_comment", wpid = db_question.id, uid = request.session.get('user_id',None), content = content, delete = False)
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "question_collection", wpid = db_question.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "question_collection", wpid = db_question.id, uid = request.session.get('user_id',None))
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            print(delete_form.is_valid())
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_coment = models.Comment.objects.get(id = delete_id)
                delete_coment.delete = True
                delete_coment.save()

    comment_list = []
    all_comment = models.Comment.objects.filter(tag = "question_comment", wpid = db_question.id, delete = False)
    for entry in all_comment:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["user_id"] = entry.uid
        new_entry["user_name"] = models.User.objects.get(id = entry.uid).name
        new_entry["content"] = entry.content
        new_entry["date"] = entry.date
        comment_list.append(new_entry)

    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "question_collection", wpid = db_question.id, uid = request.session.get('user_id',None))
            collection = "collection_button_1"
        except:
            collection = "collection_button_2"
    return render(request, 'question.html', {"question":question, "comment_list":comment_list, "collection":collection})

#搜索页
def search(request,key,w_p,tag):
    search_key = {"key":key, "w_p":w_p, "tag":tag}
    if search_key["key"] == "search_key":
        search_form = forms.SearchForm(request.POST)
        if search_form.is_valid():
            search_key["key"] = search_form.cleaned_data["search_key"]

    list = []
    if search_key["w_p"] == "work":
        if search_key["tag"] == "all":
            all = models.Work.objects.filter(name__contains = search_key["key"])
        else:
            list_1 = models.Work.objects.filter(name__contains = search_key["key"])
            list_2 = models.Tag.objects.filter(name = search_key["tag"])
            for entry in list_1:
                new_entry = {}
                new_entry["id"] = entry.id
                new_entry["name"] = entry.name
                if list_2.filter(wid = entry.id).exists():
                    list.append(new_entry)
            all = []
    else:
        all = models.Post.objects.filter(name__contains = search_key["key"], tag = search_key["w_p"])
    for entry in all:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = entry.name
        list.append(new_entry)

    tag_list = []
    all_tag = models.Tag.objects.all().values("name").distinct()
    for entry in all_tag:
        new_entry = {}
        new_entry["name"] = entry["name"]
        tag_list.append(new_entry)
    return render(request, 'search.html',{"search_key":search_key, "list":list, "tag_list":tag_list})
