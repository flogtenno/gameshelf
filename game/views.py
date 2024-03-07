from django.shortcuts import render,redirect
from .models import Game,GameComment
from .form import GameCommentForm

def game(request, game_id):

    if request.method == 'POST':
        form = GameCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.game_comment_user = request.user
            comment.game_comment_game_id = game_id
            comment.save()
            return redirect('game', game_id=game_id)

    game    = Game.objects.get(pk=game_id) # Game オブジェクトを取得
    comment = GameComment.objects.filter(game_comment_game=game)
    form    = GameCommentForm()

    params = {
        "login_user"    :   request.user, #現在のログインユーザー情報（request.user）
        "displaygame"   :   game, #game詳細情報全体
        "displaycomment":   comment, #gameに対してのコメント一覧
        "commentform"   :   form,
    }

    return render(request, 'game/game.html', params)

"""
comment.game_comment_game に game オブジェクトを直接代入する場合、game オブジェクトがまだデータベースに保存されていない可能性があります。
そのため、comment オブジェクトを保存しようとすると、Django は game オブジェクトを保存しようとしているかもしれません。
この場合、game オブジェクトには pk がないため、外部キー制約のエラーが発生します。
一方、comment.game_comment_game_id = game_id のように game_id の値を直接代入する場合、外部キー制約に違反することはありません。
外部キー制約は、関連するモデルの id（または pk）を保存するため、この方法で問題が解決されます。
したがって、comment.game_comment_game = game ではなく、comment.game_comment_game_id = game_id を使用して
game_comment_game フィールドに値を代入することで、外部キー制約に違反する可能性を回避し、正常に保存することができます。
"""