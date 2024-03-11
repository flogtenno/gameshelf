from django import forms
from.models import Diary,DiaryComment

# Messaeフォーム

class DiaryCreateForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields=["diary_title","diary_tag","diary_content"]

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

