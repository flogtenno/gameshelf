from django.db import models
from accounts.models import CustomUser
from game.models import Game
from top.models import Tag
from django.core.validators import MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

class Diary(models.Model):
    diary_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    diary_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    diary_tag = models.ManyToManyField(Tag)
    diary_title = models.CharField(max_length=100)
    diary_content = models.TextField()
    diary_rating = models.IntegerField(validators=[MaxValueValidator(100)])
    diary_spoiler = models.BooleanField(default=False) #ネタバレチェック、デフォで無し側

    def __str__(self):
        return f"{str(self.diary_title)}({str(self.diary_user)})"

    class Meta:
        ordering = ("-id",)

class DiaryImage(models.Model):
    diary_image_diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_image_image = models.ImageField(upload_to="media/")
    diary_image_comment = models.CharField(max_length=100, blank=True, null=True)
    diary_image_mainflag = models.BooleanField(default=False) #メイン画像フラグ
@receiver(post_save, sender=DiaryImage)
def ensure_single_main_flag(sender, instance, **kwargs):
    if instance.diary_image_mainflag:
        # メインフラグが日記１つに対して、フラグ１つのみになるように他を解除する
        DiaryImage.objects.filter(diary_image_diary=instance.diary_image_diary).exclude(id=instance.id).update(diary_image_mainflag=False)

class DiaryComment(models.Model):
    diary_comment_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    diary_comment_diary = models.ForeignKey(Diary, on_delete=models.CASCADE)
    diary_comment_comment = models.CharField(max_length=1000)