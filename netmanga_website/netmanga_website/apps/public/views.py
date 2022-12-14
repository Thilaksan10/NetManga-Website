import bleach
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from ..accounts.models import OneShot, Profile, Creator, MangaSeries, Chapter, ChapterImages, Subscriber, ChapterRating, ChapterComment, ChapterCommentRating, CoinOffer, Award, ChapterAward, ReportChapter, OneShotImages, OneShotRating, OneShotComment, OneShotCommentRating, OneShotAward, ReportOneShot
from .forms import CommentForm, EditPlotForm, ReportForm
from .algorithms import *
from django.forms.models import model_to_dict
import json
from django.core import serializers


def index(request):
    template = loader.get_template('index.html')
    
    if request.method == 'GET':
        mangas = MangaSeries.objects.all()
        oneshots = OneShot.objects.all()
        if request.user.is_authenticated:
            subscribed_mangas = Subscriber.objects.filter(user=request.user)
            return HttpResponse(template.render({'mangas':mangas, 'oneshots':oneshots, 'subscribed_mangas':subscribed_mangas,}, request))
        return HttpResponse(template.render({'mangas':mangas, 'oneshots':oneshots}, request))
        
    return HttpResponse(template.render({}, request))

def search(request):
    
    if request.method=="POST":
        template = loader.get_template('search.html')
        search = request.POST['search']
        mangas = MangaSeries.objects.filter(title__icontains = search)
        chapters = Chapter.objects.filter(title__icontains = search)
        oneshots = OneShot.objects.filter(title__icontains = search)
        chapter_infos=[]
        manga_infos=[]
        platinum_award = Award.objects.get(name="Platinum Award")
        gold_award = Award.objects.get(name="Gold Award")
        silver_award = Award.objects.get(name="Silver Award")
        bronce_award = Award.objects.get(name="Bronce Award")
        for chapter in chapters:
            likes = ChapterRating.objects.filter(chapter=chapter,rating=True)
            dislikes = ChapterRating.objects.filter(chapter=chapter,rating=False)
            platinum = ChapterAward.objects.filter(chapter=chapter,award=platinum_award).count()
            gold = ChapterAward.objects.filter(chapter=chapter,award=gold_award).count()
            silver = ChapterAward.objects.filter(chapter=chapter,award=silver_award).count()
            bronce = ChapterAward.objects.filter(chapter=chapter,award=bronce_award).count()
            chapter_infos.insert(0,ChapterInfo(chapter,len(likes),len(dislikes),platinum,gold,silver,bronce))
        
        for manga in mangas:
            chapters = len(Chapter.objects.filter(manga=manga))
            latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
           
            manga_infos.append(MangaInfo(manga,latest_chapter))
            mergeSort_by_latest_upload(manga_infos)
        
        return HttpResponse(template.render({'manga_infos':manga_infos, 'oneshots':oneshots, 'chapter_infos':chapter_infos,'search':search},request))
    else:
        return HttpResponseRedirect('/')
   

def popular(request):
    
    template = loader.get_template('popular.html')
    mangas = sort_view()
    oneshots = OneShot.objects.all().order_by('views')
    
    return HttpResponse(template.render({'mangas':mangas, 'oneshots':oneshots}, request))

class ChapterInfo:
    def __init__(self,chapter,likes,dislikes,platinumawards,goldawards,silverawards,bronceawards):
        self.chapter = chapter
        self.likes = likes
        self.dislikes = dislikes
        self.platinumawards = platinumawards
        self.goldawards = goldawards
        self.silverawards = silverawards
        self.bronceawards = bronceawards  

def chapterlist(request,pk):
    template =loader.get_template('chapterlist.html')
    manga = MangaSeries.objects.filter(pk=pk).first()
    chapters = Chapter.objects.filter(manga=pk).order_by('no')
    chapter_infos = []
    total_views = 0
    platinum_award = Award.objects.get(name="Platinum Award")
    gold_award = Award.objects.get(name="Gold Award")
    silver_award = Award.objects.get(name="Silver Award")
    bronce_award = Award.objects.get(name="Bronce Award")
    for chapter in chapters:
        likes = ChapterRating.objects.filter(chapter=chapter,rating=True)
        dislikes = ChapterRating.objects.filter(chapter=chapter,rating=False)
        platinum = ChapterAward.objects.filter(chapter=chapter,award=platinum_award).count()
        gold = ChapterAward.objects.filter(chapter=chapter,award=gold_award).count()
        silver = ChapterAward.objects.filter(chapter=chapter,award=silver_award).count()
        bronce = ChapterAward.objects.filter(chapter=chapter,award=bronce_award).count()
        chapter_infos.insert(0,ChapterInfo(chapter,len(likes),len(dislikes),platinum,gold,silver,bronce))
        total_views += chapter.views
    if request.method == 'GET':
        form = EditPlotForm(initial={'plot':manga.plot})
        if request.user.is_authenticated:
            subscribed = Subscriber.objects.filter(manga=manga, user=request.user).first() != None
            subscriber_count = len(Subscriber.objects.filter(manga=manga))
            return HttpResponse(template.render({'manga': manga, 'chapter_infos': chapter_infos, 'subscribed':subscribed,'subscriber_count':subscriber_count,'total_views':total_views,'form':form,},request))    
        else:
            subscriber_count = len(Subscriber.objects.filter(manga=manga))
            return HttpResponse(template.render({'manga': manga, 'chapter_infos': chapter_infos,'subscriber_count':subscriber_count,'total_views':total_views,'form':form},request))
    elif request.method =='POST':
        print('check',flush=True)
        if request.user.is_authenticated:
            print('user',flush=True)
            subscriber = Subscriber.objects.filter(manga=manga, user=request.user).first()
            form = EditPlotForm(request.POST)
            if form.is_valid():
                manga.plot=bleach.clean(form.cleaned_data['plot'])
                manga.save()
            if request.POST.get('subscribe', False) is not False:
                if subscriber is None:
                    subscriber = Subscriber.objects.create(manga=manga, user=request.user)
                    subscriber.save()
                    subscribed = True
                    subscriber_count = len(Subscriber.objects.filter(manga=manga))
                else:
                    subscriber.delete()
                    subscribed = False
                    subscriber_count = len(Subscriber.objects.filter(manga=manga))
            return HttpResponse(status=204)
            #return HttpResponse(template.render({'manga': manga, 'chapter_infos': chapter_infos,'subscribed':subscribed,'subscriber_count':subscriber_count,'total_views':total_views,'form':form},request))
        else:
            print('redirect',flush=True)
            return HttpResponseRedirect('/accounts/login')
    #return HttpResponse(template.render({},request))     

class CommentInfoJson:
    def __init__(self, comment, rating):
        self.comment = model_to_dict(comment)
        self.rating = rating

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def create_commentinfojson_list(comments, comment_ratings):
    comment_infos = []
    
    for comment in comments:
        rating = -1
        if comment_ratings:
            for comment_rating in comment_ratings:
                if comment_rating.comment.pk == comment.pk:
                    rating = int(comment_rating.rating)
       
        comment_infos.append(json.loads(CommentInfoJson(comment,rating).toJson()))

    return comment_infos

class CommentInfo:
    def __init__(self, comment, rating):
        self.comment = comment
        self.rating = rating

def create_commentinfo_list(comments, comment_ratings):
    comment_infos = []
    
    for comment in comments:
        rating = -1
        if comment_ratings:
            for comment_rating in comment_ratings:
                if comment_rating.comment.pk == comment.pk:
                    rating = int(comment_rating.rating)
       
        comment_infos.append(CommentInfo(comment,rating))

    return comment_infos

def chapter_viewer_post(request,chapter):
    reload = False
    if request.user.is_authenticated:
        if request.POST.get('subscribe', False) is not False:
            subscriber = Subscriber.objects.filter(manga=chapter.manga, user=request.user).first()
            if subscriber is None:
                subscriber = Subscriber.objects.create(manga=chapter.manga, user=request.user)
                subscriber.save()
            else:
                subscriber.delete()

        elif request.POST.get('like', False) is not False:
            rating = ChapterRating.objects.filter(chapter=chapter, user=request.user).first()
            if rating is None:
                rating = ChapterRating.objects.create(chapter=chapter, user=request.user, rating=1)
                rating.save()
            else:
                if rating.rating == 1:
                    rating.delete()
                else:
                    rating.rating = 1
                    rating.save()

        elif request.POST.get('dislike', False) is not False:
            rating = ChapterRating.objects.filter(chapter=chapter, user=request.user).first()
            if rating is None:
                rating = ChapterRating.objects.create(chapter=chapter, user=request.user, rating=0)
                rating.save()
            else:
                if rating.rating == 0:
                    rating.delete()
                else:
                    rating.rating = 0
                    rating.save()

        elif request.POST.get('award', False) is not False:
            award = Award.objects.filter(name=request.POST.get('award')).first()
            user_balance = request.user.profile.coins
            user_balance = user_balance - award.price
            
            if user_balance >= 0: 
                chapter_award = ChapterAward.objects.create(award=award, user=request.user, chapter=chapter)
                chapter_award.save()
                request.user.profile.coins = user_balance
                request.user.save() 
                creator = chapter.manga.creator
                creator.user.profile.coins += award.coins_reward
                creator.user.profile.save()
                money = creator.earned_money
                creator.earned_money = money + award.fiat_reward
                creator.save()
            reload = True
        
        elif request.POST.get('report',False) is not False:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = ReportChapter.objects.create(chapter=chapter, user=request.user)
                report.report = bleach.clean(report_form.cleaned_data['report'])
                report.save()
                report_form = ReportForm()
            reload = True

        elif request.POST.get('comment', False) is not False:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = ChapterComment.objects.create(chapter=chapter, user=request.user)
                comment.comment = bleach.clean(comment_form.cleaned_data['comment'])
                comment.save()
                comment_form = CommentForm()
            reload = True

        elif request.POST.get('commentlike', False) is not False:
            comment = ChapterComment.objects.filter(pk=int(request.POST.get('commentlike'))).first()
            comment_rating = ChapterCommentRating.objects.filter(comment=comment, user=request.user).first()
            if comment_rating is None:
                comment_rating = ChapterCommentRating.objects.create(comment=comment, user=request.user, rating=True)
                comment_rating.save()
            else:
                if comment_rating.rating == 1:
                    comment_rating.delete()
                else:
                    comment_rating.rating = 1
                    comment_rating.save()
            comment.like = len(ChapterCommentRating.objects.filter(comment=comment,rating=True))
            comment.dislike = len(ChapterCommentRating.objects.filter(comment=comment,rating=False))
            comment.save()

        elif request.POST.get('commentdislike', False) is not False:
            comment = ChapterComment.objects.filter(pk=int(request.POST.get('commentdislike'))).first()
            comment_rating = ChapterCommentRating.objects.filter(comment=comment, user=request.user).first()
            if comment_rating is None:
                comment_rating = ChapterCommentRating.objects.create(comment=comment, user=request.user, rating=False)
                comment_rating.save()
            else:
                if comment_rating.rating == 0:
                    comment_rating.delete()
                else:
                    comment_rating.rating = 0
                    comment_rating.save()
            comment.like = len(ChapterCommentRating.objects.filter(comment=comment,rating=True))
            comment.dislike = len(ChapterCommentRating.objects.filter(comment=comment,rating=False))
            comment.save()
        else:
            raise NotImplementedError
    return reload

def chapter_viewer(request,pk):
    template =loader.get_template('chapter_viewer.html')
    chapter = Chapter.objects.filter(pk=pk).first()
    chapterpages = ChapterImages.objects.filter(chapter=pk).order_by('no')
    comment_form = CommentForm()
    report_form = ReportForm()
    awards = Award.objects.all().order_by('pk')
    image_urls = []
    for chapterpage in chapterpages:
        image_urls.append(chapterpage.image.url)
    if request.method == 'GET':
        rating = ChapterRating.objects.filter(chapter=pk)
        likes = ChapterRating.objects.filter(chapter=pk, rating=True)
        dislikes = ChapterRating.objects.filter(chapter=pk, rating=False)
        comments = ChapterComment.objects.filter(chapter=pk)
        comment_ratings = None
        if request.user.is_authenticated:
            user_rating = ChapterRating.objects.filter(chapter=chapter, user=request.user).first()
            comment_ratings = ChapterCommentRating.objects.filter(comment__in=comments, user=request.user)
            subscribed = Subscriber.objects.filter(manga=chapter.manga, user=request.user).first() != None
        comment_infos = create_commentinfo_list(comments,comment_ratings)
        comment_infos_json = create_commentinfojson_list(comments,comment_ratings)
        print(comment_infos, flush=True)
        chapter.views += 1
        chapter.save()
        
        if request.user.is_authenticated:
            return HttpResponse(template.render({'chapter': chapter, 'chapterpages': chapterpages, 'json_chapterpages': serializers.serialize('json', chapterpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'user_rating': user_rating, 'subscribed': subscribed, 'comment_form': comment_form, 'awards': awards, 'report_form':report_form},request))
        else:
            return HttpResponse(template.render({'chapter': chapter, 'chapterpages': chapterpages, 'json_chapterpages': serializers.serialize('json', chapterpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'comment_form': comment_form,  'awards': awards, 'report_form':report_form},request))
    elif request.method == 'POST':
        reload = chapter_viewer_post(request,chapter)

        rating = ChapterRating.objects.filter(chapter=pk)
        likes = ChapterRating.objects.filter(chapter=pk, rating=True)
        dislikes = ChapterRating.objects.filter(chapter=pk, rating=False)
        comments = ChapterComment.objects.filter(chapter=pk)
        comment_ratings = None
        if request.user.is_authenticated:
            if not reload:
                return HttpResponse(status=204)
            else:
                user_rating = ChapterRating.objects.filter(chapter=chapter, user=request.user).first()
                comment_ratings = ChapterCommentRating.objects.filter(comment__in=comments, user=request.user)
                subscribed = Subscriber.objects.filter(manga=chapter.manga, user=request.user).first() != None
                comment_infos = create_commentinfo_list(comments,comment_ratings)
                comment_infos_json = create_commentinfojson_list(comments,comment_ratings)
                print(comment_infos, flush=True)
                return HttpResponse(template.render({'chapter': chapter, 'chapterpages': chapterpages, 'json_chapterpages': serializers.serialize('json', chapterpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'user_rating': user_rating, 'subscribed': subscribed, 'comment_form': comment_form,  'awards': awards, 'report_form':report_form},request))
        else:
            print("redirect",flush=True)
            return HttpResponseRedirect('/accounts/login')
    else:    
        pass

def oneshot_viewer_post(request,oneshot):
    reload = False
    if request.user.is_authenticated:
        if request.POST.get('like', False) is not False:
            rating = OneShotRating.objects.filter(oneshot=oneshot, user=request.user).first()
            if rating is None:
                rating = OneShotRating.objects.create(oneshot=oneshot, user=request.user, rating=1)
                rating.save()
            else:
                if rating.rating == 1:
                    rating.delete()
                else:
                    rating.rating = 1
                    rating.save()

        elif request.POST.get('dislike', False) is not False:
            rating = OneShotRating.objects.filter(oneshot=oneshot, user=request.user).first()
            if rating is None:
                rating = OneShotRating.objects.create(oneshot=oneshot, user=request.user, rating=0)
                rating.save()
            else:
                if rating.rating == 0:
                    rating.delete()
                else:
                    rating.rating = 0
                    rating.save()

        elif request.POST.get('award', False) is not False:
            award = Award.objects.filter(name=request.POST.get('award')).first()
            user_balance = request.user.profile.coins
            user_balance = user_balance - award.price
            
            if user_balance >= 0: 
                oneshot_award = OneShotAward.objects.create(award=award, user=request.user, oneshot=oneshot)
                oneshot_award.save()
                request.user.profile.coins = user_balance
                request.user.save() 
                creator = oneshot.creator
                creator.user.profile.coins += award.coins_reward
                creator.user.profile.save()
                money = creator.earned_money
                creator.earned_money = money + award.fiat_reward
                creator.save()
            reload = True
        
        elif request.POST.get('report',False) is not False:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = ReportOneShot.objects.create(oneshot=oneshot, user=request.user)
                report.report = bleach.clean(report_form.cleaned_data['report'])
                report.save()
                report_form = ReportForm()
            reload = True

        elif request.POST.get('comment', False) is not False:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = OneShotComment.objects.create(oneshot=oneshot, user=request.user)
                comment.comment = bleach.clean(comment_form.cleaned_data['comment'])
                comment.save()
                comment_form = CommentForm()
            reload = True

        elif request.POST.get('commentlike', False) is not False:
            comment = OneShotComment.objects.filter(pk=int(request.POST.get('commentlike'))).first()
            comment_rating = OneShotCommentRating.objects.filter(comment=comment, user=request.user).first()
            if comment_rating is None:
                comment_rating = OneShotCommentRating.objects.create(comment=comment, user=request.user, rating=True)
                comment_rating.save()
            else:
                if comment_rating.rating == 1:
                    comment_rating.delete()
                else:
                    comment_rating.rating = 1
                    comment_rating.save()
            comment.like = len(OneShotCommentRating.objects.filter(comment=comment,rating=True))
            comment.dislike = len(OneShotCommentRating.objects.filter(comment=comment,rating=False))
            comment.save()

        elif request.POST.get('commentdislike', False) is not False:
            comment = OneShotComment.objects.filter(pk=int(request.POST.get('commentdislike'))).first()
            comment_rating = OneShotCommentRating.objects.filter(comment=comment, user=request.user).first()
            if comment_rating is None:
                comment_rating = OneShotCommentRating.objects.create(comment=comment, user=request.user, rating=False)
                comment_rating.save()
            else:
                if comment_rating.rating == 0:
                    comment_rating.delete()
                else:
                    comment_rating.rating = 0
                    comment_rating.save()
            comment.like = len(OneShotCommentRating.objects.filter(comment=comment,rating=True))
            comment.dislike = len(OneShotCommentRating.objects.filter(comment=comment,rating=False))
            comment.save()
        else:
            raise NotImplementedError
    return reload

def oneshot_viewer(request,pk):
    template =loader.get_template('oneshot_viewer.html')
    oneshot = OneShot.objects.filter(pk=pk).first()
    oneshotpages = OneShotImages.objects.filter(oneshot=pk).order_by('no')
    comment_form = CommentForm()
    report_form = ReportForm()
    awards = Award.objects.all().order_by('pk')
    image_urls = []
    for oneshotpage in oneshotpages:
        image_urls.append(oneshotpage.image.url)
    if request.method == 'GET':
        rating = OneShotRating.objects.filter(oneshot=pk)
        likes = OneShotRating.objects.filter(oneshot=pk, rating=True)
        dislikes = OneShotRating.objects.filter(oneshot=pk, rating=False)
        comments = OneShotComment.objects.filter(oneshot=pk)
        comment_ratings = None
        if request.user.is_authenticated:
            user_rating = OneShotRating.objects.filter(oneshot=oneshot, user=request.user).first()
            comment_ratings = OneShotCommentRating.objects.filter(comment__in=comments, user=request.user)
        comment_infos = create_commentinfo_list(comments,comment_ratings)
        comment_infos_json = create_commentinfojson_list(comments,comment_ratings)
        print(comment_infos, flush=True)
        oneshot.views += 1
        oneshot.save()
        
        if request.user.is_authenticated:
            return HttpResponse(template.render({'oneshot': oneshot, 'oneshotpages': oneshotpages, 'json_oneshotpages': serializers.serialize('json', oneshotpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'user_rating': user_rating, 'comment_form': comment_form, 'awards': awards, 'report_form':report_form},request))
        else:
            return HttpResponse(template.render({'oneshot': oneshot, 'oneshotpages': oneshotpages, 'json_oneshotpages': serializers.serialize('json', oneshotpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'comment_form': comment_form,  'awards': awards, 'report_form':report_form},request))
    elif request.method == 'POST':
        reload = oneshot_viewer_post(request,oneshot)

        rating = OneShotRating.objects.filter(oneshot=pk)
        likes = OneShotRating.objects.filter(oneshot=pk, rating=True)
        dislikes = OneShotRating.objects.filter(oneshot=pk, rating=False)
        comments = OneShotComment.objects.filter(oneshot=pk)
        comment_ratings = None
        if request.user.is_authenticated:
            if not reload:
                return HttpResponse(status=204)
            else:
                user_rating = OneShotRating.objects.filter(oneshot=oneshot, user=request.user).first()
                comment_ratings = OneShotCommentRating.objects.filter(comment__in=comments, user=request.user)
                comment_infos = create_commentinfo_list(comments,comment_ratings)
                comment_infos_json = create_commentinfojson_list(comments,comment_ratings)
                print(comment_infos, flush=True)
                return HttpResponse(template.render({'oneshot': oneshot, 'oneshotpages': oneshotpages, 'json_oneshotpages': serializers.serialize('json', oneshotpages), 'image_urls': image_urls, 'likes': len(likes), 'dislikes': len(dislikes), 'comment_infos': comment_infos, 'comment_infos_json': comment_infos_json, 'user_rating': user_rating, 'comment_form': comment_form,  'awards': awards, 'report_form':report_form},request))
        else:
            print("redirect",flush=True)
            return HttpResponseRedirect('/accounts/login')
    else:    
        pass

''' All Genre related views '''
def genre(request):
    template = loader.get_template('genre.html')
    
    if request.method == 'GET':
        mangas = MangaSeries.objects.all()
        action_mangas = []
        drama_mangas = []
        comedy_mangas = []
        fantasy_mangas = []
        slice_of_life_mangas = []
        romance_mangas = []
        superhero_mangas = []
        sci_fi_mangas = []
        thriller_mangas = []
        supernatural_mangas = []
        mystery_mangas = []
        sports_mangas = []
        historical_mangas = []
        heartwarming_mangas = []
        horror_mangas = []
        informative_mangas = []
        for manga in mangas:
            if manga.primary_Genre == 'Action' or manga.secondary_Genre == 'Action':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                action_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Drama' or manga.secondary_Genre == 'Drama':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                drama_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Comedy' or manga.secondary_Genre == 'Comedy':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                comedy_mangas.append(MangaInfo(manga,latest_chapter))    
            if manga.primary_Genre == 'Fantasy' or manga.secondary_Genre == 'Fantasy':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                fantasy_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Slice of Life' or manga.secondary_Genre == 'Slice of Life':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                slice_of_life_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Romance' or manga.secondary_Genre == 'Romance':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                romance_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Superhero' or manga.secondary_Genre == 'Superhero':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                superhero_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Sci-Fi' or manga.secondary_Genre == 'Sci-Fi':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                sci_fi_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Thriller' or manga.secondary_Genre == 'Thriller':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                thriller_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Supernatural' or manga.secondary_Genre == 'Supernatural':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                supernatural_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Mystery' or manga.secondary_Genre == 'Mystery':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                mystery_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Sports' or manga.secondary_Genre == 'Sports':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                sports_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Historical' or manga.secondary_Genre == 'Historical':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                historical_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Heartwarming' or manga.secondary_Genre == 'Heartwarming':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                heartwarming_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Horror' or manga.secondary_Genre == 'Horror':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                horror_mangas.append(MangaInfo(manga,latest_chapter))
            if manga.primary_Genre == 'Informative' or manga.secondary_Genre == 'Informative':
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                informative_mangas.append(MangaInfo(manga,latest_chapter))

        oneshots = OneShot.objects.all().order_by('-published')
        action_oneshots = []
        drama_oneshots = []
        comedy_oneshots = []
        fantasy_oneshots = []
        slice_of_life_oneshots = []
        romance_oneshots = []
        superhero_oneshots = []
        sci_fi_oneshots = []
        thriller_oneshots = []
        supernatural_oneshots = []
        mystery_oneshots = []
        sports_oneshots = []
        historical_oneshots = []
        heartwarming_oneshots = []
        horror_oneshots = []
        informative_oneshots = []
        for oneshot in oneshots:
            if oneshot.primary_Genre == 'Action' or oneshot.secondary_Genre == 'Action':
                action_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Drama' or oneshot.secondary_Genre == 'Drama':
                drama_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Comedy' or oneshot.secondary_Genre == 'Comedy':
                comedy_oneshots.append(oneshot)    
            if oneshot.primary_Genre == 'Fantasy' or oneshot.secondary_Genre == 'Fantasy':
                fantasy_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Slice of Life' or oneshot.secondary_Genre == 'Slice of Life':
                slice_of_life_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Romance' or oneshot.secondary_Genre == 'Romance':
                romance_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Superhero' or oneshot.secondary_Genre == 'Superhero':
                superhero_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Sci-Fi' or oneshot.secondary_Genre == 'Sci-Fi':
                sci_fi_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Thriller' or oneshot.secondary_Genre == 'Thriller':
                thriller_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Supernatural' or oneshot.secondary_Genre == 'Supernatural':
                supernatural_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Mystery' or oneshot.secondary_Genre == 'Mystery':
                mystery_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Sports' or oneshot.secondary_Genre == 'Sports':
                sports_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Historical' or oneshot.secondary_Genre == 'Historical':
                historical_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Heartwarming' or oneshot.secondary_Genre == 'Heartwarming':
                heartwarming_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Horror' or oneshot.secondary_Genre == 'Horror':
                horror_oneshots.append(oneshot)
            if oneshot.primary_Genre == 'Informative' or oneshot.secondary_Genre == 'Informative':
                informative_oneshots.append(oneshot)

        mergeSort_by_latest_upload(action_mangas)
        mergeSort_by_latest_upload(drama_mangas)
        mergeSort_by_latest_upload(comedy_mangas)
        mergeSort_by_latest_upload(fantasy_mangas)
        mergeSort_by_latest_upload(slice_of_life_mangas)
        mergeSort_by_latest_upload(romance_mangas)
        mergeSort_by_latest_upload(superhero_mangas)
        mergeSort_by_latest_upload(sci_fi_mangas)
        mergeSort_by_latest_upload(thriller_mangas) 
        mergeSort_by_latest_upload(supernatural_mangas)
        mergeSort_by_latest_upload(mystery_mangas)
        mergeSort_by_latest_upload(sports_mangas) 
        mergeSort_by_latest_upload(historical_mangas) 
        mergeSort_by_latest_upload(heartwarming_mangas)
        mergeSort_by_latest_upload(horror_mangas)
        mergeSort_by_latest_upload(informative_mangas) 
        return HttpResponse(template.render({'action_mangas':action_mangas, 'drama_mangas':drama_mangas, 'comedy_mangas':comedy_mangas, 'fantasy_mangas':fantasy_mangas, 'slice_of_life_mangas':slice_of_life_mangas, 'romance_mangas':romance_mangas, 'superhero_mangas':superhero_mangas, 'sci_fi_mangas':sci_fi_mangas, 'thriller_mangas':thriller_mangas, 'supernatural_mangas':supernatural_mangas, 'mystery_mangas':mystery_mangas, 'sports_mangas':sports_mangas, 'historical_mangas':historical_mangas,'heartwarming_mangas':heartwarming_mangas, 'horror_mangas':horror_mangas, 'informative_mangas':informative_mangas, 'action_oneshots':action_oneshots, 'drama_oneshots':drama_oneshots, 'comedy_oneshots':comedy_oneshots, 'fantasy_oneshots':fantasy_oneshots, 'slice_of_life_oneshots':slice_of_life_oneshots, 'romance_oneshots':romance_oneshots, 'superhero_oneshots':superhero_oneshots, 'sci_fi_oneshots':sci_fi_oneshots, 'thriller_oneshots':thriller_oneshots, 'supernatural_oneshots':supernatural_oneshots, 'mystery_oneshots':mystery_oneshots, 'sports_oneshots':sports_oneshots, 'historical_oneshots':historical_oneshots,'heartwarming_oneshots':heartwarming_oneshots, 'horror_oneshots':horror_oneshots, 'informative_oneshots':informative_oneshots}, request))
    return HttpResponse(template.render({}, request))

def action(request):
    template = loader.get_template('genre/action.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Action')
        return HttpResponse(template.render({'mangas': mangas,}, request))  
    return HttpResponse(template.render({}, request))

def drama(request):
    template = loader.get_template('genre/drama.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Drama') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def comedy(request):
    template = loader.get_template('genre/comedy.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Comedy')
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def fantasy(request):
    template = loader.get_template('genre/fantasy.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Fantasy') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def slice_of_life(request):
    template = loader.get_template('genre/slice_of_life.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Slice of Life') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def romance(request):
    template = loader.get_template('genre/romance.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Romance') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def superhero(request):
    template = loader.get_template('genre/superhero.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Superhero') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def sci_fi(request):
    template = loader.get_template('genre/sci-fi.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Sci-Fi') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def thriller(request):
    template = loader.get_template('genre/thriller.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Thriller') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def supernatural(request):
    template = loader.get_template('genre/supernatural.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Supernatural') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def mystery(request):
    template = loader.get_template('genre/mystery.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Mystery') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def sports(request):
    template = loader.get_template('genre/sports.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Sports') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def historical(request):
    template = loader.get_template('genre/historical.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Historical') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def heartwarming(request):
    template = loader.get_template('genre/heartwarming.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Heartwarming') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def horror(request):
    template = loader.get_template('genre/horror.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Horror') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

def informative(request):
    template = loader.get_template('genre/informative.html')
    
    if request.method == 'GET':
        mangas = sort_view_of_genre('Informative') 
        return HttpResponse(template.render({'mangas': mangas,}, request))
    return HttpResponse(template.render({}, request))

''' All Footer Views '''

def about(request):
    template = loader.get_template('footer/about.html')
    
    return HttpResponse(template.render({}, request))

def user_terms(request):
    template = loader.get_template('footer/user_terms.html')
    
    return HttpResponse(template.render({}, request))

def creator_terms(request):
    template = loader.get_template('footer/creator_terms.html')
    
    return HttpResponse(template.render({}, request))

def privacy_policy(request):
    template = loader.get_template('footer/privacy_policy.html')
    
    return HttpResponse(template.render({}, request))