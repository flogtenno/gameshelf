from django.shortcuts import render,redirect
from .models import Diary,DiaryComment,DiaryImage
from .forms import DiaryCommentForm,DiaryCreateForm
from django.contrib import messages #メッセージの送信完了をおしらせ


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
        "displayimage"   :   image,
        "displaycomment" :   comment, #diaryに対してのコメント一覧
        "commentform"    :   form,
    }

    return render(request, 'diary/diary.html', params)

def newdiary(request):
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES) #request.FILESが無いとファイルの登録不可、注意
        if form.is_valid():
            diary = form.save()
            messages.success(request, "作成しました")
            return redirect('diary', diary_id=diary.id) #diary = form.save()でdiaryに丸々保存内容が入っている、diary.idを指定して新規作成したページへ飛べる

    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "createform"    :   DiaryCreateForm(),
    }

    return render(request, 'diary/newdiary.html', params)

def editdiary(request, diary_id):
    editdiary = Diary.objects.get(pk=diary_id)
    if request.method == 'POST':
        form = DiaryCreateForm(request.POST, request.FILES, instance=editdiary) #request.FILESが無いとファイルの登録不可、注意
        if form.is_valid():
            diary = form.save()
            messages.success(request, "編集しました")
            return redirect('diary', diary_id=diary.id)
    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "editdiary"     :   editdiary,
        "editform"      :   DiaryCreateForm(instance=editdiary)
    }
    return render(request, "diary/editdiary.html", params)

"""
comment.diary_comment_diary に diary オブジェクトを直接代入する場合、diary オブジェクトがまだデータベースに保存されていない可能性があります。
そのため、comment オブジェクトを保存しようとすると、Django は diary オブジェクトを保存しようとしているかもしれません。
この場合、diary オブジェクトには pk がないため、外部キー制約のエラーが発生します。
一方、comment.diary_comment_diary_id = diary_id のように diary_id の値を直接代入する場合、外部キー制約に違反することはありません。
外部キー制約は、関連するモデルの id（または pk）を保存するため、この方法で問題が解決されます。
したがって、comment.diary_comment_diary = diary ではなく、comment.diary_comment_diary_id = diary_id を使用して
diary_comment_diary フィールドに値を代入することで、外部キー制約に違反する可能性を回避し、正常に保存することができます。
"""