from django.shortcuts import render,redirect
from django.contrib import messages #メッセージの送信完了をおしらせ
from django.core.paginator import Paginator #ページ区切り
from django.db.models import Q
from .forms import CreateTagForm
from .models import Tag
from diary.models import Diary,DiaryImage
from game.models import Game
from django.core.exceptions import ObjectDoesNotExist

# トップページ（目次）___________________________________________________________________
def top (request):
    first_three_diary = Diary.objects.all()[:3]
    first_four_game = Game.objects.all()[:4]

    main_img_set(first_three_diary) #メイン画像セット関数

    params={
        "login_user"         :   request.user, #現在のログインユーザー情報（request.user）
        "first_three_diary"  :   first_three_diary,
        "first_four_game"   :   first_four_game, #指定されたページのポストが格納されている。HTMLで表示するため。
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
    diary_paginator = Paginator(hit_diaries, 4) #4つで区切る
    game_paginator = Paginator(hit_game, 4) #4つで区切る
    diary_page_number = request.GET.get('diary-page', 1) #HTML側からページの要求があるので保存
    game_page_number = request.GET.get('game-page', 1) #初期値は1
    diary_display_page = diary_paginator.get_page(diary_page_number) #要求のあったページ情報を保存
    game_display_page = game_paginator.get_page(game_page_number)

    main_img_set(diary_display_page) #メインフラグのついた画像をセット

    params={
        "searchword"         :   tag,
        "diary_display_page" :   diary_display_page,
        "game_display_page"  :   game_display_page,
    }
    return render(request, "top/search.html", params)

# キーワード検索___________________________________________________________________
def keyword_search(request):
    keyword = request.GET.get('keyword') #検索キーワードの取得

    # ゲームの検索
    game_results = Game.objects.filter(Q(game_title__icontains=keyword) | Q(game_content__icontains=keyword) | Q(game_tag__tag__icontains=keyword)).distinct()

    # 日記の検索
    diary_results = Diary.objects.filter(Q(diary_title__icontains=keyword) | Q(diary_content__icontains=keyword) | Q(diary_tag__tag__icontains=keyword)).distinct()

    game_paginator = Paginator(game_results, 4) # ページネーション
    diary_paginator = Paginator(diary_results, 4)

    game_page_number = request.GET.get('game-page',1) #対象のページ取得
    diary_page_number = request.GET.get('diary-page',1)

    game_page_result = game_paginator.get_page(game_page_number) # 対象のページを変数に保存
    diary_page_result = diary_paginator.get_page(diary_page_number)

    main_img_set(diary_page_result) #メインフラグのついた画像をセット

    params = {
        'searchword'        : keyword,
        'diary_display_page': diary_page_result,
        'game_display_page' : game_page_result,
    }

    return render(request, 'top/search.html', params)

# main画像設定関数___________________________________________________________________
def main_img_set(temp):
    for diary in temp:
        try: #メインフラグが１つもなかった場合のエラー対策の為、tryで実行
            main_image = DiaryImage.objects.get(diary_image_diary=diary, diary_image_mainflag=True) #メインフラグのついた画像を取得する
        except ObjectDoesNotExist:
            main_image = None  # メイン画像が存在しない場合は None を設定
        diary.main_image = main_image  # 日記に main_image 属性を追加 diary.main_imageで引っ張れる
        if diary.main_image:
            print(f"***メイン画像セット***タイトル:{diary.diary_title} メイン画像URL:{diary.main_image.diary_image_image.url}***") #メイン画像が取得できてるか？
    return
