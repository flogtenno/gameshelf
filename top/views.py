from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
# from django.contrib import messages #メッセージの送信完了をおしらせ
# from django.core.paginator import Paginator #ページ区切り
# from django.db.models import Q
from django.contrib.auth.decorators import login_required

# from .models import Message,Good
# from .forms import MessageForm

# top（目次）___________________________________________________________________
def top (request):
    params={
        "login_user"     :   request.user, #現在のログインユーザー情報（request.user）
        "title"          :   "GameShelf", #保存用のModelForm、保存先はMessage
        "image1"         :   "/gameshelf.jpg", #指定されたページのポストが格納されている。HTMLで表示するため。
    }
    return render(request, "top/top.html", params)