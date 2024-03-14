from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from django.core.paginator import Paginator #ページ区切り
# from django.db.models import Q
from .forms import CreateTagForm
from .models import Tag
from diary.models import Diary
from game.models import Game

# トップページ（目次）___________________________________________________________________
def top (request):
    params={
        "login_user"     :   request.user, #現在のログインユーザー情報（request.user）
        "title"          :   "GameShelf",
        "image1"         :   "/gameshelf.jpg", #指定されたページのポストが格納されている。HTMLで表示するため。
    }

    return render(request, "top/top.html", params)

# Tag追加________________________________________________________________________
def tag(request):
    form = CreateTagForm()
    alltags = Tag.objects.all()
    if request.method == 'POST':
        print("***Tag保存開始***")
        form = CreateTagForm(request.POST)
        if form.is_valid():
            new_tag = form.cleaned_data['tag'] #フォーム内のtagを取り出して比較させる
            if not Tag.objects.filter(tag=new_tag).exists(): #もし既存のタグと内容が同じならTrueなので、notで否定
                form.save()
                print("***Tag保存完了***")
                messages.success(request, f"「{new_tag}」タグを追加しました")
            else:
                print("***Tag保存失敗***")
                messages.error(request, "このタグは既に存在します")
            return redirect('tag')  # どちらの分岐でもリダイレクト
    params={
        "createform":   form,
        "alltags"   :   alltags,
    }
    return render(request, 'top/tag.html', params)

# Tag検索______________________________________________________________________

def tag_search(request, tag_id):
    tag = Tag.objects.get(id=tag_id) #IDをもとに、どのタグで検索がされたのかを特定
    hit_diaries = Diary.objects.filter(diary_tag=tag) #データ全体から、タグの内容が一致するレコードを取り出す
    hit_game = Game.objects.filter(game_tag=tag)
    # print(f"*****diary:{hit_diaries}*****")
    # print(f"*****game:{hit_game}*****")
    diary_paginator = Paginator(hit_diaries, 3) #3つで区切る
    game_paginator = Paginator(hit_game, 3) #3つで区切る
    diary_page_number = request.GET.get('diary-page', 1) #HTML側からページの要求があるので保存
    game_page_number = request.GET.get('game-page', 1) #初期値は1
    diary_display_page = diary_paginator.get_page(diary_page_number) #要求のあったページ情報を保存
    game_display_page = game_paginator.get_page(game_page_number)
    params={
        "tagname"            :   tag,
        "diary_display_page" :   diary_display_page,
        "game_display_page"  :   game_display_page,
    }
    return render(request, "top/search.html", params)
