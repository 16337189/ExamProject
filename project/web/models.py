from django.db import models

#用户
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    password = models.TextField()
    email = models.TextField()
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#作品
class Work(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    date = models.TextField()
    introduction = models.TextField()
    class Meta:
        verbose_name = '作品'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#分数
class Score(models.Model):
    wid = models.IntegerField()
    uid = models.IntegerField()
    name = models.TextField()
    score = models.IntegerField()
    main = models.BooleanField()
    class Meta:
        verbose_name = '分数'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#标签
class Tag(models.Model):
    wid = models.IntegerField()
    uid = models.IntegerField()
    name = models.TextField()
    main = models.BooleanField()
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#帖子
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.TextField()
    uid = models.IntegerField()
    name = models.TextField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField()
    class Meta:
        verbose_name = '帖子'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

#评论
class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.TextField()
    wpid = models.IntegerField()
    uid = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    delete = models.BooleanField()
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.tag

#收藏
class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    tag = models.TextField()
    wpid = models.IntegerField()
    uid = models.IntegerField()
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.tag
