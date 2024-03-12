from django import forms
from.models import Game,GameComment
from top.models import Tag

# Messaeフォーム

class GameCommentForm(forms.ModelForm): #保存用にModelFormを使う
    class Meta:
        model=GameComment #参照先のテーブル（モデル）
        fields=["game_comment_comment"]
        widgets={
            "game_comment_comment": forms.Textarea(attrs={"class":"form-control form-control-sm","rows": 1}),
        }
        labels = {
            "game_comment_comment": "",  # ラベルを空に設定する
        }

class GameCreateForm(forms.ModelForm):
    game_tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Game
        fields=["game_title","game_tag","game_content","game_image"]