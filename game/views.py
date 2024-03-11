from django.shortcuts import render,redirect
from .models import Game,GameComment
from .forms import GameCommentForm,GameCreateForm
from django.contrib import messages #メッセージの送信完了をおしらせ


def game(request, game_id):

    if request.method == 'POST':
        form = GameCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) #フォームの関連付けをしてから保存は一旦待つ
            comment.game_comment_user = request.user #コメントはだれが行ったかを保存
            comment.game_comment_game_id = game_id #コメントの際にはフォームに"{% url 'game' displaygame.id %}"の記載がある。game_idが本ページのIDとして利用可能
            comment.save()
            return redirect('game', game_id=game_id) #path('<int:game_id>', views.game,name="game"),

    game    = Game.objects.get(pk=game_id) # Game オブジェクトを取得、gameIDを主キーとしてGET
    comment = GameComment.objects.filter(game_comment_game=game) #game_comment_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    form    = GameCommentForm() #コメント入力用フォーム

    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "displaygame"   :   game, #game詳細情報全体
        "displaycomment":   comment, #gameに対してのコメント一覧
        "commentform"   :   form,
    }

    return render(request, 'game/game.html', params)

def newgame(request):
    if request.method == 'POST':
        form = GameCreateForm(request.POST, request.FILES) #request.FILESが無いとファイルの登録不可、注意
        if form.is_valid():
            game = form.save()
            messages.success(request, "作成しました")
            return redirect('game', game_id=game.id) #game = form.save()でgameに丸々保存内容が入っている、game.idを指定して新規作成したページへ飛べる

    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "createform"    :   GameCreateForm(),
    }

    return render(request, 'game/newgame.html', params)

def editgame(request, game_id):
    editgame = Game.objects.get(pk=game_id)
    if request.method == 'POST':
        form = GameCreateForm(request.POST, request.FILES, instance=editgame) #request.FILESが無いとファイルの登録不可、注意
        if form.is_valid():
            game = form.save()
            messages.success(request, "編集しました")
            return redirect('game', game_id=game.id)
    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "editgame"      :   editgame,
        "editform"      :   GameCreateForm(instance=editgame)
    }
    return render(request, "game/editgame.html", params)

"""
comment.game_comment_game に game オブジェクトを直接代入する場合、game オブジェクトがまだデータベースに保存されていない可能性があります。
そのため、comment オブジェクトを保存しようとすると、Django は game オブジェクトを保存しようとしているかもしれません。
この場合、game オブジェクトには pk がないため、外部キー制約のエラーが発生します。
一方、comment.game_comment_game_id = game_id のように game_id の値を直接代入する場合、外部キー制約に違反することはありません。
外部キー制約は、関連するモデルの id（または pk）を保存するため、この方法で問題が解決されます。
したがって、comment.game_comment_game = game ではなく、comment.game_comment_game_id = game_id を使用して
game_comment_game フィールドに値を代入することで、外部キー制約に違反する可能性を回避し、正常に保存することができます。
"""