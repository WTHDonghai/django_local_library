"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include,path,re_path
from catalog.urls import urlpatterns as catalogUrl
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^catalog/',include('catalog.urls')),

    #将根目录url(127.0.0.1:8000)重定向到项目应用的url(127.0.0.1:8000/catalog/)
    re_path(r'^$',RedirectView.as_view(url='/catalog/',permanent = True)),
]



#映射静态文件
from django.conf.urls.static import static 
from django.conf import settings

urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_URL)


#登陆系统，Add Django site authentication urls(for login,logout,passwrod management)
urlpatterns += [
        path('accounts/',include('django.contrib.auth.urls')),
] 

