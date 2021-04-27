from django.contrib import admin

from .models import Profile, Creator, Mangaseries, Chapter, Chapterimages, Rating, Subscriber, Comment, CommentRating, CoinOffer, Award, ChapterAward, ReportChapter, CoinPurchaseOrder

admin.site.register(Profile)
admin.site.register(Creator)
admin.site.register(Mangaseries)
admin.site.register(Chapter)
admin.site.register(Chapterimages)
admin.site.register(Rating)
admin.site.register(Subscriber)
admin.site.register(Comment)
admin.site.register(CommentRating)
admin.site.register(CoinOffer)
admin.site.register(Award)
admin.site.register(ChapterAward)
admin.site.register(ReportChapter)
admin.site.register(CoinPurchaseOrder)
