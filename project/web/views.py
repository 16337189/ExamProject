from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Avg
from django.db.models import Count
from . import models
from . import forms
import random
from operator import attrgetter

#主页
def home(request):
    #作品列表
    new_list = list(models.Post.objects.filter(tag = "work"))
    all_work = random.sample(new_list,10 if len(new_list) > 10 else len(new_list))
    work_list = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = models.Work.objects.get(id = entry.cid).name
        work_list.append(new_entry)

    #讨论列表
    new_list = list(models.Post.objects.filter(tag = "disscussion"))
    all_disscussion = random.sample(new_list,5 if len(new_list) > 5 else len(new_list))
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        disscussion_list.append(new_entry)

    #问题列表
    new_list = list(models.Post.objects.filter(tag = "question"))
    all_question = random.sample(new_list,5 if len(new_list) > 5 else len(new_list))
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        question_list.append(new_entry)

    example = {"work_list":work_list, "disscussion_list":disscussion_list, "question_list":question_list}
    return render(request, 'home.html', {"example":example})

#登录
def signin(request):
    #判断是否登录
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
    #判断是否登录
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
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                else:
                    same_email_user = models.User.objects.filter(email=email)
                    if same_email_user:
                        message = '该邮箱地址已被注册，请使用别的邮箱！'
                    else:
                        models.User.objects.create(name = username, password = password1, email = email)
                        return redirect('/signin')
        return render(request, 'login.html', {"message":message})
    return render(request, 'login.html')

#注销
def logout(request):
    #判断是否登录
    if not request.session.get('is_login', None):
        return redirect("/home")
    request.session.flush()
    return redirect("/home")

#用户页
def user(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')

    #推荐列表
    tag={}
    all_collection = models.Collection.objects.filter(tag = "work_collection", uid = request.session.get('user_id',None))
    include_wid = []
    for entry in all_collection:
        wid =  models.Post.objects.get(id = entry.pid).cid
        include_wid.append(wid)
        all_tag = models.Tag.objects.filter(wid = wid).values("name").distinct()
        for entry2 in all_tag:
            if entry2["name"] not in tag.keys():
                tag[entry2["name"]] = 1
            else:
                tag[entry2.name] = tag[entry2.name] + 1
    tag = sorted(tag.items(), key = lambda entry:entry[1], reverse=True)
    list = []
    for entry in tag:
        wid = models.Tag.objects.filter(name = entry[0]).values("wid").distinct()
        for entry2 in wid:
            if entry2["wid"] not in include_wid:
                new_entry = {}
                new_entry["id"] = models.Post.objects.get(tag = "work", cid =entry2["wid"]).id
                new_entry["name"] = models.Work.objects.get(id = entry2["wid"]).name
                list.append(new_entry)
            if len(list) > 4:
                break
        if len(list) > 4:
            break

    return render(request, 'user.html', {"list":list})

#用户收藏页
def user_collection(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')

    #收藏作品列表
    all_work = models.Collection.objects.filter(tag = "work_collection", uid = request.session.get('user_id',None))
    work_list = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.pid
        new_entry["name"] = models.Work.objects.get(id = models.Post.objects.get(id = entry.pid).cid).name
        work_list.append(new_entry)

    #收藏讨论列表
    all_disscussion = models.Collection.objects.filter(tag = "disscussion_collection", uid = request.session.get('user_id',None))
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.pid
        new_entry["title"] = models.Disscussion.objects.get(id = models.Post.objects.get(id = entry.pid).cid).title
        disscussion_list.append(new_entry)

    #收藏问题列表
    all_question = models.Collection.objects.filter(tag = "question_collection", uid = request.session.get('user_id',None))
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.pid
        new_entry["title"] = models.Disscussion.objects.get(id = models.Post.objects.get(id = entry.pid).cid).title
        question_list.append(new_entry)

    collection = {"work_list":work_list, "disscussion_list":disscussion_list, "question_list":question_list}
    return render(request, 'user_collection.html', {"collection":collection})

#用户帖子页
def user_post(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')

    #自己的作品列表
    all_work = models.Post.objects.filter(tag = "work", uid = request.session.get('user_id',None))
    work_list = []
    for entry in all_work:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["name"] = models.Work.objects.get(id = entry.cid).name
        work_list.append(new_entry)

    #自己的讨论列表
    all_disscussion = models.Post.objects.filter(tag = "disscussion", uid = request.session.get('user_id',None))
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        disscussion_list.append(new_entry)

    #自己的问题列表
    all_question = models.Post.objects.filter(tag = "question", uid = request.session.get('user_id',None))
    question_list = []
    for entry in all_question:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        question_list.append(new_entry)

    written = {"work_list":work_list, "disscussion_list":disscussion_list, "question_list":question_list}
    return render(request, 'user_post.html', {"written":written})

#用户私信页
def user_message(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')

    #私信列表
    message_list = []
    all_message = models.Message.objects.filter(rid = request.session.get('user_id',None))
    for entry in all_message:
        post = models.Post.objects.get(tag = "message", cid = entry.id)
        new_entry = {}
        new_entry["writter_id"] = post.uid
        new_entry["writter_name"] = models.User.objects.get(id = post.uid).name
        new_entry["content"] = entry.content
        new_entry["date"] = post.date
        message_list.append(new_entry)

    message_list = sorted(message_list, key=lambda entey: entey["date"], reverse = True)

    return render(request, 'user_message.html', {"message_list":message_list})

#私信编写页
def write_message(request,id):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        message_form = forms.MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data["message"]
            message = models.Message.objects.create(rid = id, content = content)
            post = models.Post.objects.create(tag = "message", uid = request.session.get('user_id',None), cid = message.id, delete = False)
            return redirect('/user/')
    return render(request, 'write_message.html')

#作品总页
def works(request,carry,year,tag,sort):
    #载体和年份筛选
    if carry != "all":
        if year !=  "all":
            all_work = models.Work.objects.filter(carry= carry, year = year)
        else:
            all_work = models.Work.objects.filter(carry= carry)
    else:
        if year !=  "all":
            all_work = models.Work.objects.filter(year = year)
        else:
            all_work = models.Work.objects.all()
    work_list = []
    #标签筛选
    if tag != "all":
        list_1 = models.Tag.objects.filter(name = tag)
        for entry in all_work:
            if list_1.filter(wid = entry.id).exists():
                post = models.Post.objects.get(tag = "work", cid = entry.id)
                new_entry = {}
                new_entry["id"] = post.id
                new_entry["name"] = entry.name
                new_entry["date"] = post.date
                new_entry["score"] = models.Score.objects.filter(wid = entry.id, name = "总分").aggregate(avg_s=Avg("score"))["avg_s"]
                if not new_entry["score"]:
                    new_entry["score"] = 0
                work_list.append(new_entry)
    else:
        for entry in all_work:
            post = models.Post.objects.get(tag = "work", cid = entry.id)
            new_entry = {}
            new_entry["id"] = post.id
            new_entry["name"] = entry.name
            new_entry["date"] = post.date
            new_entry["score"] = models.Score.objects.filter(wid = entry.id, name = "总分").aggregate(avg_s=Avg("score"))["avg_s"]
            if not new_entry["score"]:
                new_entry["score"] = 0
            work_list.append(new_entry)

    #排序
    sort_key = sort.split(':', 1 )
    if len(sort_key) < 2:
        work_list = sorted(work_list, key=lambda entey: entey[sort_key[0]])
    else:
        work_list = sorted(work_list, key=lambda entey: entey[sort_key[0]], reverse = True)

    #载体列表
    carry_list = models.Work.objects.all().values("carry").distinct()

    #年份列表
    year_list = models.Work.objects.all().values("year").distinct()

    #标签列表
    tag_list = models.Tag.objects.all().values("name").distinct()

    screening_key = {"carry":carry, "year":year, "tag":tag, "sort":sort}
    screening_list = {"carry_list":carry_list, "year_list":year_list, "tag_list":tag_list}

    return render(request, 'works.html', {"work_list":work_list, "screening_key":screening_key, "screening_list":screening_list})

#作品推荐编写页
def write_work(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        work_form = forms.WorkForm(request.POST)
        if work_form.is_valid():
            name = work_form.cleaned_data["name"]
            carry = work_form.cleaned_data["carry"]
            year = work_form.cleaned_data["year"]
            introduction = work_form.cleaned_data["introduction"]
            work = models.Work.objects.create(name = name, carry = carry, year = year, introduction = introduction)
            post = models.Post.objects.create(tag = "work", uid = request.session.get('user_id',None), cid = work.id, delete = False)
            return redirect('/work/'+str(post.id))
    return render(request, 'write_work.html')

#作品推荐重写页
def rewriter_work(request,id):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    post = models.Post.objects.get(id = id)
    if request.method == "POST":
        work_form = forms.WorkForm(request.POST)
        if work_form.is_valid():
            work = models.Work.objects.get(id = post.cid)
            work.name = work_form.cleaned_data["name"]
            work.carry = work_form.cleaned_data["carry"]
            work.year = work_form.cleaned_data["year"]
            work.introduction = work_form.cleaned_data["introduction"]
            work.save()
            return redirect('/work/'+str(post.id))

    work = models.Work.objects.get(id = post.cid)
    text = {}
    text["name"] = work.name
    text["carry"] = work.carry
    text["year"] = work.year
    text["introduction"] = work.introduction
    return render(request, 'rewrite_work.html', {"text":text})

#作品页
def work(request,id):
    #获取作品数据
    db_post =  models.Post.objects.get(id = id)
    post = {}
    post["writter_id"] = db_post.uid
    post["writter_name"] = models.User.objects.get(id = db_post.uid).name
    post["date"] = db_post.date
    db_work = models.Work.objects.get(id = db_post.cid)
    work = {}
    work["name"] = db_work.name
    work["carry"] = db_work.carry
    work["year"] = db_work.year
    work["introduction"] = db_work.introduction

    #判断表单是否提交
    if request.method == "POST" and request.session.get('is_login',None):
        #评论提交
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                comment = models.Comment.objects.create(pid = db_post.id, tag = "usual", content = content)
                models.Post.objects.create(tag = "work_comment", uid = request.session.get('user_id',None), cid = comment.id, delete = False)
        #评分提交
        if "score_update" in request.POST:
            score_form = forms.ScoreForm(request.POST)
            if score_form.is_valid():
                score = score_form.cleaned_data["score"]
                try:
                    new_score = models.Score.objects.get(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分")
                    new_score.score = score
                    new_score.save()
                except:
                    models.Score.objects.create(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分", score = score)
        #收藏提交
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "work_collection", pid = db_post.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "work_collection", pid = db_post.id, uid = request.session.get('user_id',None))
        #标签提交
        if "tag_update" in request.POST:
            tag_form = forms.TagForm(request.POST)
            if tag_form.is_valid():
                tag_name = tag_form.cleaned_data["tag_name"]
                try:
                    models.Tag.objects.get(wid = db_work.id, uid = request.session.get('user_id',None)).delete()
                except:
                    tag_name = tag_form.cleaned_data["tag_name"]
                models.Tag.objects.create(wid = db_work.id, uid = request.session.get('user_id',None), name = tag_name)
        #评论删除
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_post = models.Post.objects.get(id = delete_id)
                delete_post.delete = True
                delete_post.save()

    #评论列表
    comment_list = []
    all_comment = models.Comment.objects.filter(pid = db_post.id)
    for entry in all_comment:
        c_post = models.Post.objects.get(tag = "work_comment", cid = entry.id)
        if c_post.delete == False:
            new_entry = {}
            new_entry["id"] = c_post.id
            new_entry["writter_id"] = c_post.uid
            new_entry["writter_name"] = models.User.objects.get(id = c_post.uid).name
            new_entry["content"] = entry.content
            new_entry["date"] = c_post.date
            comment_list.append(new_entry)

    #评分计算
    score = {}
    score["avg_s"] = models.Score.objects.filter(wid = db_work.id, name = "总分").aggregate(avg_s=Avg("score"))["avg_s"]
    try:
        score["user_s"] = models.Score.objects.get(wid = db_work.id, uid = request.session.get('user_id',None), name = "总分").score
    except:
        score["user_s"] = False

    #收藏判断
    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "work_collection", pid = db_post.id, uid = request.session.get('user_id',None))
            collection = "collection_button_1"
        except:
            collection = "collection_button_2"

    #标签列表
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

    #相似作品推荐列表
    choose_work_id = sorted(choose_work_id.items(), key = lambda kv:kv[1], reverse=True)
    choose_work_list = []
    counter = 0
    for entry in choose_work_id:
        if counter >= 5:
            break
        new_entry = {}
        new_entry["id"] = models.Post.objects.get(tag = "work", cid = entry[0]).id
        new_entry["name"] = models.Work.objects.get(id = entry[0]).name
        choose_work_list.append(new_entry)
        counter = counter + 1
    return render(request, 'work.html', {"post":post, "work":work, "comment_list":comment_list, "score":score, "collection":collection, "tag_list":tag_list, "choose_work_list":choose_work_list})

#讨论总页
def disscussions(request):
    all_disscussion = models.Post.objects.filter(tag = "disscussion")
    disscussion_list = []
    for entry in all_disscussion:
        new_entry = {}
        new_entry["id"] = entry.id
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        disscussion_list.append(new_entry)
    return render(request, 'disscussions.html', {"disscussion_list":disscussion_list})

#讨论编写页
def write_disscussion(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            disscussion = models.Disscussion.objects.create(title = title, content = content)
            post = models.Post.objects.create(tag ="disscussion", uid = request.session.get('user_id',None), cid = disscussion.id, delete = False)
            return redirect('/disscussion/'+str(post.pk))
    return render(request, 'write_disscussion.html')

#讨论重写页
def rewriter_disscussion(request,id):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    post = models.Post.objects.get(id = id)
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            disscussion = models.Disscussion.objects.get(id = post.cid)
            disscussion.title = post_form.cleaned_data["title"]
            disscussion.content = post_form.cleaned_data["content"]
            disscussion.save()
            return redirect('/disscussion/'+str(post.id))

    disscussion = models.Disscussion.objects.get(id = post.cid)
    text = {}
    text["title"] = disscussion.title
    text["content"] = disscussion.content
    return render(request, 'rewrite_disscussion.html', {"text":text})

#讨论页
def disscussion(request,id):
    #获取讨论数据
    db_post = models.Post.objects.get(id = id)
    db_disscussion = models.Disscussion.objects.get(pk = db_post.cid)
    disscussion = {}
    disscussion["title"] = db_disscussion.title
    disscussion["content"] = db_disscussion.content
    disscussion["writter_id"] = db_post.uid
    disscussion["writter_name"] =  models.User.objects.get(id = db_post.uid).name
    disscussion["date"] = db_post.date

    #判断表单是否提交
    if request.method == "POST" and request.session.get('is_login',None):
        #评论提交
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                comment = models.Comment.objects.create(pid = db_post.id, tag = "usual", content = content)
                models.Post.objects.create(tag = "disscussion_comment", uid = request.session.get('user_id',None), cid = comment.id, delete = False)
        #收藏提交
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "disscussion_collection", pid = db_post.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "disscussion_collection", pid = db_post.id, uid = request.session.get('user_id',None))
        #评论删除
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_post = models.Post.objects.get(id = delete_id)
                delete_post.delete = True
                delete_post.save()

    #评论列表
    comment_list = []
    all_comment = models.Comment.objects.filter(pid = db_post.id)
    for entry in all_comment:
        c_post = models.Post.objects.get(tag = "disscussion_comment", cid = entry.id)
        if c_post.delete == False:
            new_entry = {}
            new_entry["id"] = c_post.id
            new_entry["writter_id"] = c_post.uid
            new_entry["writter_name"] = models.User.objects.get(id = c_post.uid).name
            new_entry["content"] = entry.content
            new_entry["date"] = c_post.date
            comment_list.append(new_entry)

    #收藏判断
    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "disscussion_collection", pid = db_post.id, uid = request.session.get('user_id',None))
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
        new_entry["title"] = models.Disscussion.objects.get(id = entry.cid).title
        question_list.append(new_entry)
    return render(request, 'questions.html', {"question_list":question_list})

#问题编写页
def write_question(request):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            title = post_form.cleaned_data["title"]
            content = post_form.cleaned_data["content"]
            question = models.Disscussion.objects.create(title = title, content = content)
            post = models.Post.objects.create(tag ="question", uid = request.session.get('user_id',None), cid = question.id, delete = False)
            return redirect('/question/'+str(post.id))
    return render(request, 'write_question.html')

#问题重写页
def rewriter_question(request,id):
    #判断是否登录
    if not request.session.get('is_login',None):
        return redirect('/home')
    post = models.Post.objects.get(id = id)
    if request.method == "POST":
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            question = models.Disscussion.objects.get(id = post.cid)
            question.title = post_form.cleaned_data["title"]
            question.content = post_form.cleaned_data["content"]
            question.save()
            return redirect('/question/'+str(post.id))

    question = models.Disscussion.objects.get(id = post.cid)
    text = {}
    text["title"] = question.title
    text["content"] = question.content
    return render(request, 'rewrite_question.html', {"text":text})

#问题页
def question(request,id):
    #获取问题数据
    db_post = models.Post.objects.get(id = id)
    db_question = models.Disscussion.objects.get(id = db_post.cid)
    question = {}
    question["title"] = db_question.title
    question["content"] = db_question.content
    question["writter_id"] = db_post.uid
    question["writter_name"] =  models.User.objects.get(id = db_post.uid).name
    question["date"] = db_post.date

    #判断表单是否提交
    if request.method == "POST" and request.session.get('is_login',None):
        #评论提交
        if "comment_update" in request.POST:
            comment_form = forms.CommentForm(request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data["content"]
                comment = models.Comment.objects.create(pid = db_post.id, tag = "usual", content = content)
                models.Post.objects.create(tag = "question_comment", uid = request.session.get('user_id',None), cid = comment.id, delete = False)
        #收藏提交
        if "collection_update" in request.POST:
            try:
                models.Collection.objects.get(tag = "question_collection", pid = db_post.id, uid = request.session.get('user_id',None)).delete()
            except:
                models.Collection.objects.create(tag = "question_collection", pid = db_post.id, uid = request.session.get('user_id',None))
        #评论删除
        if "comment_delete" in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                delete_id = delete_form.cleaned_data["delete_id"]
                delete_post = models.Post.objects.get(id = delete_id)
                delete_post.delete = True
                delete_post.save()
        #最佳答案提交
        if "answer_update" in request.POST:
            best_form = forms.BestForm(request.POST)
            if best_form.is_valid():
                best_id = best_form.cleaned_data["best_id"]
                try:
                    best_comment = models.Comment.objects.get(pid = db_post.id, tag = "best")
                    if best_comment.id != best_id:
                        best_comment.tag = "usual"
                        best_comment.save()
                except:
                    best_comment = []
                best_comment = models.Comment.objects.get(id = models.Post.objects.get(id = best_id).cid)
                best_comment.tag = "best"
                best_comment.save()

    #评论列表
    comment_list = []
    all_comment = models.Comment.objects.filter(pid = db_post.id)
    for entry in all_comment:
        c_post = models.Post.objects.get(tag = "question_comment", cid = entry.id)
        if c_post.delete == False:
            new_entry = {}
            new_entry["id"] = c_post.id
            new_entry["writter_id"] = c_post.uid
            new_entry["writter_name"] = models.User.objects.get(id = c_post.uid).name
            new_entry["content"] = entry.content
            new_entry["date"] = c_post.date
            comment_list.append(new_entry)
    try:
        b_c = models.Comment.objects.get(pid = db_post.id, tag = "best")
        c_post = models.Post.objects.get(tag = "question_comment", cid = b_c.id)
        if c_post.delete == False:
            best_comment = {"writter_name": models.User.objects.get(id = c_post.uid).name,"content": b_c.content, "date":c_post.date}
        else:
            best_comment = False
    except:
        best_comment = False

    #收藏判断
    collection = ""
    if request.session.get('is_login',None):
        try:
            models.Collection.objects.get(tag = "question_collection", pid = db_post.id, uid = request.session.get('user_id',None))
            collection = "collection_button_1"
        except:
            collection = "collection_button_2"
    return render(request, 'question.html', {"question":question, "comment_list":comment_list, "best_comment":best_comment, "collection":collection})

#搜索页
def search(request,key,w_p,tag):
    search_key = {"key":key, "w_p":w_p, "tag":tag}
    #确定搜索关键字
    if search_key["key"] == "search_key":
        search_form = forms.SearchForm(request.POST)
        if search_form.is_valid():
            search_key["key"] = search_form.cleaned_data["search_key"]

    list = []
    #确定帖子类型和标签
    if search_key["w_p"] == "work":
        if search_key["tag"] == "all":
            all_work = models.Work.objects.all()
            for entry in all_work:
                if search_key["key"] in entry.name or search_key["key"] in entry.introduction:
                    post = models.Post.objects.get(tag = "work", cid = entry.id)
                    new_entry = {}
                    new_entry["id"] =  post.id
                    new_entry["name"] = entry.name
                    list.append(new_entry)
        else:
            all_work = models.Work.objects.all()
            tag_choose_list = models.Tag.objects.filter(name = search_key["tag"])
            for entry in all_work:
                if search_key["key"] in entry.name or search_key["key"] in entry.introduction:
                    if tag_choose_list.filter(wid = entry.id).exists():
                        post = models.Post.objects.get(tag = "work", cid = entry.id)
                        new_entry = {}
                        new_entry["id"] =  post.id
                        new_entry["name"] = entry.name
                        list.append(new_entry)
    else:
        all_post = models.Post.objects.filter(tag = search_key["w_p"])
        for entry in all_post:
            d_q = models.Disscussion.objects.get(id = entry.cid)
            if search_key["key"] in d_q.title or search_key["key"] in d_q.content:
                new_entry = {}
                new_entry["id"] = entry.id
                new_entry["name"] = d_q.title
                list.append(new_entry)

    #标签列表
    tag_list = models.Tag.objects.all().values("name").distinct()
    return render(request, 'search.html',{"search_key":search_key, "list":list, "tag_list":tag_list})
