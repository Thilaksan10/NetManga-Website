from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AbstractUserAdmin

from .models import User, Profile, Creator, MangaSeries, Chapter, ChapterImages, ChapterRating, Subscriber, ChapterComment, ChapterCommentRating, CoinOffer, Award, ChapterAward, ReportChapter, CoinPurchaseOrder, WithdrawOrder, OneShot, OneShotImages, OneShotComment, OneShotCommentRating, OneShotRating, OneShotAward, ReportOneShot

class UserAdmin(AbstractUserAdmin):
    model = User

admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Creator)
admin.site.register(MangaSeries)
admin.site.register(Chapter)
admin.site.register(ChapterImages)
admin.site.register(ChapterRating)
admin.site.register(Subscriber)
admin.site.register(ChapterComment)
admin.site.register(ChapterCommentRating)
admin.site.register(CoinOffer)
admin.site.register(Award)
admin.site.register(ChapterAward)
admin.site.register(ReportChapter)
admin.site.register(CoinPurchaseOrder)
admin.site.register(WithdrawOrder)
admin.site.register(OneShot)
admin.site.register(OneShotImages)
admin.site.register(OneShotRating)
admin.site.register(OneShotComment)
admin.site.register(OneShotCommentRating)
admin.site.register(OneShotAward)
admin.site.register(ReportOneShot)