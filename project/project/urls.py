"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web import views as web_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("home/", web_views.home),
    path("signin/", web_views.signin),
    path("login/", web_views.login),
    path('logout/', web_views.logout),
    path('user/', web_views.user),
    path('work/', web_views.works),
    path('write/work/', web_views.write_work),
    path('work/<int:id>/', web_views.work),
    path('disscussion/', web_views.disscussions),
    path('write/disscussion/', web_views.write_disscussion),
    path('disscussion/<int:id>/', web_views.disscussion),
    path('question/', web_views.questions),
    path('write/question/', web_views.write_question),
    path('question/<int:id>/', web_views.question),
    path('search/<str:key>/<str:tag>/', web_views.search),
]
