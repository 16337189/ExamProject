from django import forms

class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.CharField()

class WorkForm(forms.Form):
    name = forms.CharField()
    date = forms.CharField()
    introduction = forms.CharField()

class CommentForm(forms.Form):
    content = forms.CharField()

class ScoreForm(forms.Form):
    score = forms.IntegerField()

class PostForm(forms.Form):
    name = forms.CharField()
    content = forms.CharField()

class SearchForm(forms.Form):
    search_key = forms.CharField()

class TagForm(forms.Form):
    tag_name = forms.CharField()
