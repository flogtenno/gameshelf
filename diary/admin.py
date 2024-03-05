from django.contrib import admin
from .models import Diary, DiaryImage, DiaryComment

admin.site.register(Diary)
admin.site.register(DiaryImage)
admin.site.register(DiaryComment)
