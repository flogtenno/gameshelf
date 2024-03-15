from django.shortcuts import render,redirect
from .models import Diary,DiaryComment,DiaryImage
from .forms import DiaryCommentForm,DiaryCreateForm,DiaryImageForm
from django.contrib import messages #メッセージの送信完了をおしらせ

# 日記ページ表示～～～～～～～～～～～～～～～～～～～～～～～～～～～～
def diary(request, diary_id):
    if request.method == 'POST':
        form = DiaryCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) #フォームの関連付けをしてから保存は一旦待つ
            comment.diary_comment_user = request.user #コメントはだれが行ったかを保存
            comment.diary_comment_diary_id = diary_id #コメントの際にはフォームに"{% url 'diary' displaydiary.id %}"の記載がある。diary_idが本ページのIDとして利用可能
            comment.save()
            return redirect('diary', diary_id=diary_id) #path('<int:diary_id>', views.diary,name="diary"),

    diary       = Diary.objects.get(pk=diary_id) # diary オブジェクトを取得、diaryIDを主キーとしてGET
    image       = DiaryImage.objects.filter(diary_image_diary=diary) #diary_image_diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    comment     = DiaryComment.objects.filter(diary_comment_diary=diary) #diary_comment_diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    form        = DiaryCommentForm() #コメント入力用フォーム

    params = {
        "login_user"     :   request.user, #現在のログインユーザー情報（request.user）
        "displaydiary"   :   diary, #diary詳細情報全体
        "displayimage"   :   image, #画像（複数可）
        "displaycomment" :   comment, #diaryに対してのコメント一覧
        "commentform"    :   form, #コメント入力用フォーム
    }

    if diary.diary_spoiler: #ネタバレ(diary_spoiler)がTrueなら注意メッセージを表示
        messages.warning(request, "※※ネタバレを含みます※※")

    return render(request, 'diary/diary.html', params)

# 日記ページ新規作成～～～～～～～～～～～～～～～～～～～～～～～～～～～～
def newdiary(request, game_id):
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES) #request.FILESが無いとファイルの登録不可、注意
        if form.is_valid():
            temp = form.save(commit=False) #保存先との関連付けを行う
            temp.diary_user = request.user
            temp.diary_game_id = game_id
            temp.save()
            form.save_m2m() # 多対多の関係を持つタグの保存
            messages.success(request, "作成しました")
            return redirect('diary', diary_id=temp.id) #diary = form.save()でdiaryに丸々保存内容が入っている、diary.idを指定して新規作成したページへ飛べる
    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "createform"    :   DiaryCreateForm(),
        "game_id"       :   game_id,
    }
    return render(request, 'diary/newdiary.html', params)

# 日記ページ編集～～～～～～～～～～～～～～～～～～～～～～～～～～～～
def editdiary(request, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    if request.user.id == editdiary.diary_user_id: #編集リクエスト者と、記事作成者が同一かのチェック
        print("***ユーザー情報一致***")
        params = {
            "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
            "editdiary"     :   editdiary,
            "editform"      :   DiaryCreateForm(instance=editdiary)
        }
        return render(request, "diary/editdiary.html", params)
    else:
        print("***ユーザー情報不一致***")
        messages.error(request, "ユーザー情報不一致")
        return redirect('diary', diary_id=editdiary.id)


def save_editdiary(request, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    form = DiaryCreateForm(request.POST, instance=editdiary)
    if form.is_valid():
        form.save()
        messages.success(request, "編集しました")
        return redirect('diary', diary_id=editdiary.id)
    else:
        print("***入力情報エラー***")
        messages.error(request, "入力情報エラー")
        return redirect('diary', diary_id=editdiary.id)

# 日記への画像追加~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def addimagediary(request, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    image     = DiaryImage.objects.filter(diary_image_diary=editdiary) #diary_image_diary = models.ForeignKey(Diary, on_delete=models.CASCADE)

    if request.user.id == editdiary.diary_user_id: #編集リクエスト者と、記事作成者が同一かのチェック
        print("***ユーザー情報一致***")
        params = {
            "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
            "editdiary"     :   editdiary,
            "editform"      :   DiaryImageForm(),
            "displayimage"  :   image, #画像（複数可）
        }
        return render(request, "diary/addimagediary.html", params)
    else:
        print("***ユーザー情報不一致***")
        messages.error(request, "ユーザー情報不一致")
        return redirect('diary', diary_id=editdiary.id)


def save_addimagediary(request, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    form = DiaryImageForm(request.POST, request.FILES)
    if form.is_valid():
        diary_image = form.save(commit=False) # Diary インスタンスと関連付ける
        diary_image.diary_image_diary = editdiary #どのDiaryに紐づく画像かを記録
        diary_image.save()
        if request.POST.get('submit_action') == 'add_and_stay': #留まる場合
            messages.success(request, "画像を追加しました")
            return redirect('addimagediary', diary_id=editdiary.id)  # 成功時のリダイレクト先を指定
        else:
            messages.success(request, "画像を追加しました")
            return redirect('diary', diary_id=editdiary.id)  # 成功時のリダイレクト先を指定
    else:
        print("***入力情報エラー***")
        messages.error(request, "入力情報エラー")
        return redirect('diary', diary_id=editdiary.id)

# 日記の画像削除~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def deleteimagediary(request, image_id, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    deleteimage = DiaryImage.objects.get(id=image_id)
    if request.method == 'POST':
        deleteimage.delete()
        messages.success(request, "削除しました")
    else:
        messages.error(request, "削除失敗")
    return redirect('addimagediary', diary_id=editdiary.id)  # 成功時のリダイレクト先を指定

# 日記の画像にメインフラグ付与～～～～～～～～～～～～～～～～～～～～～～～～～～～～
def set_mainflag(request, diary_id, image_id):
    editdiary = Diary.objects.get(pk=diary_id)
    mainimage = DiaryImage.objects.get(id=image_id)

    if request.method == 'POST':
        mainimage.diary_image_mainflag = True
        mainimage.save()
        messages.success(request, "メイン画像を設定しました")
        return redirect('addimagediary', diary_id=editdiary.id)

    return redirect('addimagediary', diary_id=editdiary.id)  # 成功時のリダイレクト先を指定
"""
comment.diary_comment_diary に diary オブジェクトを直接代入する場合、diary オブジェクトがまだデータベースに保存されていない可能性があります。
そのため、comment オブジェクトを保存しようとすると、Django は diary オブジェクトを保存しようとしているかもしれません。
この場合、diary オブジェクトには pk がないため、外部キー制約のエラーが発生します。
一方、comment.diary_comment_diary_id = diary_id のように diary_id の値を直接代入する場合、外部キー制約に違反することはありません。
外部キー制約は、関連するモデルの id（または pk）を保存するため、この方法で問題が解決されます。
したがって、comment.diary_comment_diary = diary ではなく、comment.diary_comment_diary_id = diary_id を使用して
diary_comment_diary フィールドに値を代入することで、外部キー制約に違反する可能性を回避し、正常に保存することができます。
"""