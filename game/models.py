from django.db import models

# Create your models here.
from top.models import Tag
from accounts.models import CustomUser

class Game(models.Model):
    game_tag = models.ManyToManyField(Tag)
    game_title = models.CharField(max_length=100)
    game_content = models.TextField()
    game_image = models.ImageField(upload_to="media/", blank=True, null=True)

class GameComment(models.Model):
    game_comment_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    game_comment_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_comment_comment = models.CharField(max_length=1000)