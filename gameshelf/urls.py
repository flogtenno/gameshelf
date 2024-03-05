"""
URL configuration for gameshelf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include #includeを追加し、外部参照できるようにする

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',include("top.urls")), #ブラウザからの要求が第一引数の文字列と一致した時、include先を参照する
    # path('accounts/', include("accounts.urls")),
    # path('diary/', include("diary.urls")),
    # path('game/', include("game.urls")),
]
