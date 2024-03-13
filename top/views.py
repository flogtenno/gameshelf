from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from django.core.paginator import Paginator #ページ区切り
# from django.db.models import Q
from .forms import CreateTagForm
from .models import Tag

# トップページ（目次）___________________________________________________________________
def top (request):
    params={
        "login_user"     :   request.user, #現在のログインユーザー情報（request.user）
        "title"          :   "GameShelf", #保存用のModelForm、保存先はMessage
        "image1"         :   "/gameshelf.jpg", #指定されたページのポストが格納されている。HTMLで表示するため。
    }

    # messages.success(request, "test")

    return render(request, "top/top.html", params)

# Tag追加________________________________________________________________________
def tag(request):
    form = CreateTagForm()
    alltags = Tag.objects.all()
    if request.method == 'POST':
        form = CreateTagForm(request.POST)
        if form.is_valid():
            new_tag = form.cleaned_data['tag'] #フォーム内のtagを取り出して比較させる
            if not Tag.objects.filter(tag=new_tag).exists(): #もし既存のタグと内容が同じならTrueなので、notで否定
                form.save()
                messages.success(request, f"「{new_tag}」タグを追加しました")
            else:
                messages.error(request, "このタグは既に存在します")
            return redirect('tag')  # 成功した場合はリダイレクト
    params={
        "createform":   form,
        "alltags"   :   alltags,
    }
    return render(request, 'top/tag.html', params)

# Tag検索______________________________________________________________________

def tag_search(request, tag_id):

    pass

