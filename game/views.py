from django.shortcuts import render
from .models import Game

def game(request, game_id):
    # Game オブジェクトを取得
    game = Game.objects.get(pk=game_id)

    # テンプレートに渡すコンテキストを定義
    params = {
        'displaygame': game,
    }
    # テンプレートをレンダリングしてレスポンスを返す
    return render(request, 'game/game.html', params)
