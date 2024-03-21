from django import forms
from.models import Diary,DiaryComment,DiaryImage
from top.models import Tag

class DiaryCreateForm(forms.ModelForm):
    diary_tag = forms.ModelMultipleChoiceField(label="タグ（複数選択可能）",queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Diary
        fields = ["diary_title", "diary_tag", "diary_rating", "diary_content", "diary_spoiler"]

        labels = {
            "diary_title"   : "タイトル",
            "diary_rating"  : "スコア（最大１００点）",  # ラベルを空に設定する
            "diary_content" : "本文",
            "diary_spoiler" : "ネタバレ警告(チェックを付けると警告メッセージを表示します)"
            }


class DiaryCommentForm(forms.ModelForm): #保存用にModelFormを使う
    class Meta:
        model=DiaryComment #参照先のテーブル（モデル）
        fields=["diary_comment_comment"]
        widgets={
            "diary_comment_comment": forms.Textarea(attrs={"class":"form-control form-control-sm","rows": 1}),
        }
        labels = {
            "diary_comment_comment": "",  # ラベルを空に設定する
        }

class DiaryImageForm(forms.ModelForm):
    class Meta:
        model = DiaryImage
        fields = ['diary_image_image', 'diary_image_comment']
        labels = {
            'diary_image_image': '画像',
            'diary_image_comment': 'コメント',
        }