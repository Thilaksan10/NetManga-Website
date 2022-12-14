from curses.ascii import HT
from django.forms.widgets import NullBooleanSelect
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth import login, authenticate, tokens
from django.urls import reverse
from django.forms import modelformset_factory
from .algorithms import *
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from datetime import date, timedelta
from decimal import Decimal
import datetime

import json
import bleach

from .forms import SignUpForm, LoginForm, CreatorForm, MangaForm, ChapterForm, EditProfileForm, EditMangaForm, WithdrawForm, OneShotForm, EditOneShotForm, ResetPasswordForm

from .models import User, OneShotAward, Profile, Creator, MangaSeries, Chapter, ChapterImages, CoinOffer, Award, CoinPurchaseOrder, ChapterAward, Subscriber, WithdrawOrder, OneShot, OneShotImages



class ProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        template=loader.get_template('accounts/profile.html')
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        profile = Profile.objects.filter(user=request.user).first()
        creator = Creator.objects.filter(user=request.user).first()
        created_manga_view_tuples = sort_view(creator)
        subscribed_mangas = Subscriber.objects.filter(user=request.user)
        form=EditProfileForm(initial={'bio':profile.bio, 'display_Full_Name':profile.is_full_name_displayed})
        return HttpResponse(template.render({'profile':profile, 'created_mangas':created_manga_view_tuples, 'subscribed_mangas':subscribed_mangas,'form':form,'coinoffers':coinoffers}, request))

    def post(self, request, *args, **kwargs):
        template=loader.get_template('accounts/profile.html')
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        form=EditProfileForm(request.POST, request.FILES or None)
        profile = Profile.objects.filter(user=request.user).first()
        print("POST", flush=True)
        print("valid:" + str(form.is_valid()))
        if form.is_valid():
            if form.cleaned_data['profile_Picture'] != None:
                profile.profile_picture = form.cleaned_data['profile_Picture']
            profile.bio = bleach.clean(form.cleaned_data['bio'])
            print("Hey", flush=True)
            print("first: " + profile.bio, flush=True)
            print("second: " + bleach.clean(form.cleaned_data['bio']), flush=True)
            profile.is_full_name_displayed = form.cleaned_data['display_Full_Name']
            profile.save()
        creator = Creator.objects.filter(user=request.user).first()
        created_manga_view_tuples = sort_view(creator)
        subscribed_mangas = Subscriber.objects.filter(user=request.user)
        return HttpResponse(template.render({'profile':profile, 'created_mangas':created_manga_view_tuples, 'subscribed_mangas':subscribed_mangas,'form':form,'coinoffers':coinoffers}, request))
           
def show_profile(request,pk):
    template=loader.get_template('accounts/profile.html')
    coinoffers = CoinOffer.objects.all().order_by('pk') 
    profile = Profile.objects.filter(user=pk).first()
    creator = Creator.objects.filter(user=pk).first()
    created_manga_view_tuples = sort_view(creator)
    subscribed_mangas= None
    
    if request.method == "GET":
        form=EditProfileForm(initial={'bio':profile.bio, 'display_Full_Name':profile.is_full_name_displayed})
        if request.user == creator:
            subscribed_mangas = Subscriber.objects.filter(user=request.user)
            return HttpResponse(template.render({'profile':profile, 'created_mangas':created_manga_view_tuples, 'subscribed_mangas':subscribed_mangas,'form':form,'coinoffers':coinoffers}, request))
        else:
            return HttpResponse(template.render({'profile':profile, 'created_mangas':created_manga_view_tuples,'form':form,'coinoffers':coinoffers}, request))
    elif request.method == "POST":
        form=EditProfileForm(request.POST, request.FILES or None)
        if form.is_valid():
            if form.cleaned_data['profile_Picture'] != None:
                profile.profile_picture = form.cleaned_data['profile_Picture']
            profile.bio = bleach.clean(form.cleaned_data['bio'])
            print("Hey", flush=True)
            print("first: " + profile.bio, flush=True)
            print("second: " + bleach.clean(form.cleaned_data['bio']), flush=True)
            profile.is_full_name_displayed = form.cleaned_data['display_Full_Name']
            profile.save()
        return HttpResponse(template.render({'profile':profile, 'created_mangas':created_manga_view_tuples, 'subscribed_mangas':subscribed_mangas,'form':form,'coinoffers':coinoffers}, request))
        

class AnalyticsView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/analytics.html'
    def get(self, request, *args, **kwargs):
        template=loader.get_template('accounts/analytics.html')
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            mangas = MangaSeries.objects.filter(creator=existing_creator)
            oneshots = OneShot.objects.filter(creator=existing_creator)
            total_views = 0
            total_subscriptions = 0
            received_awards = 0
            for manga in mangas:
                #print(manga.title)
                chapters = Chapter.objects.filter(manga=manga)
                subscribers = Subscriber.objects.filter(manga=manga).count()
                total_subscriptions += subscribers
                #print('Total Subscriptions: ' + str(total_subscriptions))
                #print('Subscribers: ' + str(subscribers))
                for chapter in chapters:
                    #print(chapter.title)
                    total_views += chapter.views
                    #print('Total Views: ' + str(total_views))
                    #print('Views: ' + str(chapter.views),flush=True)
                    chapterawards = ChapterAward.objects.filter(chapter = chapter).count()
                    received_awards += chapterawards
                    #print('Total Awards: ' + str(received_awards))
                    #print('Awards: ' + str(chapterawards), flush=True)
            for oneshot in oneshots:
                total_views += oneshot.views
                received_awards += OneShotAward.objects.filter(oneshot = oneshot).count()
            days = []
            subscriptions = []
            bronce_awards = []
            silver_awards = []
            gold_awards = []
            platinum_awards = []
            revenue = []
            bronce_award = Award.objects.filter(name='Bronce Award').first()
            silver_award = Award.objects.filter(name='Silver Award').first()
            gold_award = Award.objects.filter(name='Gold Award').first()
            platinum_award = Award.objects.filter(name='Platinum Award').first()
            for i in range(27):
                days.insert(0,(date.today()-timedelta(days=i)).isoformat())
                subscription = 0
                bronce_manga_award = 0
                silver_manga_award = 0
                gold_manga_award = 0
                platinum_manga_award = 0
                for manga in mangas:
                    if i < 7:
                        chapters = Chapter.objects.filter(manga=manga)
                        
                        for chapter in chapters:
                            bronce_manga_award += ChapterAward.objects.filter(award=bronce_award,chapter=chapter,date=days[0]).count()
                            silver_manga_award += ChapterAward.objects.filter(award=silver_award,chapter=chapter,date=days[0]).count()
                            gold_manga_award += ChapterAward.objects.filter(award=gold_award,chapter=chapter,date=days[0]).count()
                            platinum_manga_award += ChapterAward.objects.filter(award=platinum_award,chapter=chapter,date=days[0]).count()
                    
                    subscription += Subscriber.objects.filter(manga=manga,date=days[0]).count()
                subscriptions.insert(0,subscription)

                for oneshot in oneshots:
                    if i < 7:
                        bronce_manga_award += OneShotAward.objects.filter(award=bronce_award,oneshot=oneshot,date=days[0]).count()
                        silver_manga_award += OneShotAward.objects.filter(award=silver_award,oneshot=oneshot,date=days[0]).count()
                        gold_manga_award += OneShotAward.objects.filter(award=gold_award,oneshot=oneshot,date=days[0]).count()
                        platinum_manga_award += OneShotAward.objects.filter(award=platinum_award,oneshot=oneshot,date=days[0]).count()

                if i<7:
                    bronce_awards.insert(0,bronce_manga_award)
                    silver_awards.insert(0,silver_manga_award)
                    gold_awards.insert(0,gold_manga_award)
                    platinum_awards.insert(0,platinum_manga_award)
                    revenue.insert(0,float(bronce_awards[0]*bronce_award.fiat_reward+silver_awards[0]*silver_award.fiat_reward+gold_awards[0]*gold_award.fiat_reward+platinum_awards[0]*platinum_award.fiat_reward))

                
            daily_subscriptions_data = {
                'labels':days,
                'data': subscriptions
            }
            daily_awards_data = {
                'labels':days[-7:],
                'data': [{
                    'bronce':bronce_awards,
                    'silver':silver_awards,
                    'gold':gold_awards,
                    'platinum':platinum_awards
                }]
            }
            
            daily_revenue_data = {
                'labels':days[-7:],
                'data':revenue
            }
            
            form = WithdrawForm()

            return HttpResponse(template.render({'total_views':total_views,'total_subscriptions':total_subscriptions,'received_awards':received_awards,'daily_subscriptions_data':daily_subscriptions_data,'daily_awards_data':daily_awards_data,'daily_revenue_data':daily_revenue_data, 'form':form}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self, request, *args, **kwargs):
        template=loader.get_template('accounts/analytics.html')
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            mangas = MangaSeries.objects.filter(creator=existing_creator)
            total_views = 0
            total_subscriptions = 0
            received_awards = 0
            for manga in mangas:
                #print(manga.title)
                chapters = Chapter.objects.filter(manga=manga)
                subscribers = Subscriber.objects.filter(manga=manga).count()
                total_subscriptions += subscribers
                #print('Total Subscriptions: ' + str(total_subscriptions))
                #print('Subscribers: ' + str(subscribers))
                for chapter in chapters:
                    #print(chapter.title)
                    total_views += chapter.views
                    #print('Total Views: ' + str(total_views))
                    #print('Views: ' + str(chapter.views),flush=True)
                    chapterawards = ChapterAward.objects.filter(chapter = chapter).count()
                    received_awards += chapterawards
                    #print('Total Awards: ' + str(received_awards))
                    #print('Awards: ' + str(chapterawards), flush=True)
            days = []
            subscriptions = []
            bronce_chapterawards = []
            silver_chapterawards = []
            gold_chapterawards = []
            platinum_chapterawards = []
            revenue = []
            bronce_award = Award.objects.filter(name='Bronce Award').first()
            silver_award = Award.objects.filter(name='Silver Award').first()
            gold_award = Award.objects.filter(name='Gold Award').first()
            platinum_award = Award.objects.filter(name='Platinum Award').first()
            for i in range(27):
                days.insert(0,(date.today()-timedelta(days=i)).isoformat())
                subscription = 0
                bronce_chapteraward = 0
                silver_chapteraward = 0
                gold_chapteraward = 0
                platinum_chapteraward = 0
                for manga in mangas:
                    if i < 7:
                        chapters = Chapter.objects.filter(manga=manga)
                        
                        for chapter in chapters:
                            bronce_chapteraward += ChapterAward.objects.filter(award=bronce_award,chapter=chapter,date=days[0]).count()
                            silver_chapteraward += ChapterAward.objects.filter(award=silver_award,chapter=chapter,date=days[0]).count()
                            gold_chapteraward += ChapterAward.objects.filter(award=gold_award,chapter=chapter,date=days[0]).count()
                            platinum_chapteraward += ChapterAward.objects.filter(award=platinum_award,chapter=chapter,date=days[0]).count()
                    
                    subscription += Subscriber.objects.filter(manga=manga,date=days[0]).count()
                subscriptions.insert(0,subscription)
                if i<7:
                    bronce_chapterawards.insert(0,bronce_chapteraward)
                    silver_chapterawards.insert(0,silver_chapteraward)
                    gold_chapterawards.insert(0,gold_chapteraward)
                    platinum_chapterawards.insert(0,platinum_chapteraward)
                    revenue.insert(0,bronce_chapterawards[0]*bronce_award.fiat_reward+silver_chapterawards[0]*silver_award.fiat_reward+gold_chapterawards[0]*gold_award.fiat_reward+platinum_chapterawards[0]*platinum_award.fiat_reward)

                
            daily_subscriptions_data = {
                'labels':days,
                'data': subscriptions
            }
            daily_awards_data = {
                'labels':days[-7:],
                'data': [{
                    'bronce':bronce_chapterawards,
                    'silver':silver_chapterawards,
                    'gold':gold_chapterawards,
                    'platinum':platinum_chapterawards
                }]
            }
            
            daily_revenue_data = {
                'labels':days[-7:],
                'data':revenue
            }
            
            form = WithdrawForm(request.POST)
            print("Form", flush=True)
            if form.is_valid():
                amount = Decimal(form.cleaned_data['amount'])
                print(existing_creator.earned_money, flush=True)
                print(amount, flush=True)
                if(amount >= existing_creator.earned_money):
                    return HttpResponse(template.render({'total_views':total_views,'total_subscriptions':total_subscriptions,'received_awards':received_awards,'daily_subscriptions_data':daily_subscriptions_data,'daily_awards_data':daily_awards_data,'daily_revenue_data':daily_revenue_data, 'form':form, 'error':0}, request))
                elif(amount < 50):
                    return HttpResponse(template.render({'total_views':total_views,'total_subscriptions':total_subscriptions,'received_awards':received_awards,'daily_subscriptions_data':daily_subscriptions_data,'daily_awards_data':daily_awards_data,'daily_revenue_data':daily_revenue_data, 'form':form, 'error':1}, request))
                paypal = form.cleaned_data['paypal']
                status = 'Pending' 
                withdraw_order = WithdrawOrder.objects.create(creator=existing_creator.user, paypal=paypal, amount=amount, status=status)
                existing_creator.earned_money = existing_creator.earned_money - withdraw_order.amount
                existing_creator.save()
                return HttpResponseRedirect('/accounts/withdraw_order')
            else:
                return HttpResponse(template.render({'total_views':total_views,'total_subscriptions':total_subscriptions,'received_awards':received_awards,'daily_subscriptions_data':daily_subscriptions_data,'daily_awards_data':daily_awards_data,'daily_revenue_data':daily_revenue_data, 'form':form, 'error':2}, request))
            
        else:
            return HttpResponseRedirect('/accounts/profile')

class UploadView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/upload.html'
    def get(self, request, *args, **kwargs):
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        template=loader.get_template('accounts/upload.html')
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            mangaseries = MangaSeries.objects.filter( creator=existing_creator)
            oneshots = OneShot.objects.filter(creator=existing_creator).order_by('published')
            manga_infos = []
            for manga in mangaseries:
                chapters = len(Chapter.objects.filter(manga=manga))
                latest_chapter = Chapter.objects.filter(manga=manga,no=chapters).first()
                print('lenght: ' + str(chapters), flush=True)
                print('latest Chapter: ' + str(latest_chapter),flush=True)
                manga_infos.append(MangaInfo(manga,latest_chapter))
            mergeSort_by_latest_upload(manga_infos)
            return HttpResponse(template.render({'manga_infos': manga_infos,'oneshots': oneshots,'coinoffers':coinoffers}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

class CreatorTermsView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/creator_terms.html'
    def get(self, request, *args, **kwargs):
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is None:
            form = CreatorForm()
            template = loader.get_template('accounts/creator_terms.html')
            return HttpResponse(template.render({'form': form,'coinoffers':coinoffers}, request))
        else:
            return HttpResponseRedirect('/terms')

    def post(self, request, *args, **kwargs):
        form = CreatorForm(request.POST)
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        if form.is_valid():
            creator = Creator.objects.create(
                user = User.objects.get(pk=request.user.id)
            )
            creator.save()
            template=loader.get_template('accounts/profile.html')
            return HttpResponseRedirect('/accounts/profile')

class NewMangaFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/new_manga_form.html'
    def get(self, request, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            form=MangaForm()
            template = loader.get_template('accounts/new_manga_form.html')
            return HttpResponse(template.render({'form': form}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self, request, *args, **kwargs):
        form = MangaForm(request.POST,request.FILES or None)
        print(request.POST, flush=True)
        template = loader.get_template('accounts/new_manga_form.html')
        if form.is_valid():
            creator = Creator.objects.filter(user=request.user).first()
            title = bleach.clean(form.cleaned_data['title'])
            cover_picture = form.cleaned_data['cover_picture']
            plot = bleach.clean(form.cleaned_data['plot'])
            primary_Genre = bleach.clean(form.cleaned_data['primary_Genre'])
            secondary_Genre = bleach.clean(form.cleaned_data['secondary_Genre'])
            if(primary_Genre == 'Select' or secondary_Genre == 'Select'):
                print('invalid_genre', flush=True)
                return HttpResponse(template.render({'form': form, 'success': False, 'invalid_genre': True}, request))
            mangaseries = MangaSeries.objects.create(creator=creator,title=title,cover_picture=cover_picture,plot=plot,primary_Genre=primary_Genre,secondary_Genre=secondary_Genre)
            pk = mangaseries.pk
            mangaseries.save()
            print(mangaseries, flush=True) 
            return HttpResponseRedirect('/accounts/new_chapter_form/'+ str(pk))
        else:
            print('Form invalid', flush = True)
            return HttpResponse(template.render({'form': form, 'success': False}, request))

class NewChapterFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/new_chapter_form.html'
    def get(self, request, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            chapterform=ChapterForm()
            template = loader.get_template('accounts/new_chapter_form.html')
            return HttpResponse(template.render({'chapterform': chapterform}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self,request,pk,*args,**kwargs):
        images = request.FILES.getlist('images')
        mangaseries = MangaSeries.objects.filter(pk=pk).first()
        chapterform=ChapterForm(request.POST)
        template = loader.get_template('accounts/new_chapter_form.html')   
        if chapterform.is_valid():
            manga = mangaseries
            title = bleach.clean(chapterform.cleaned_data['title'])
            chapter_no = self.total_chapters(mangaseries) + 1
            chapter = Chapter.objects.create(manga=manga,title=title,no=chapter_no)
            no = 1
            for image in images:
                print(image, flush=True)
                chapterimage = ChapterImages.objects.create(chapter=chapter,image=image,no=no)
                no += 1

            return HttpResponseRedirect("/accounts/profile")
        else:
            print('Form invalid', flush = True)
            return HttpResponse(template.render({'chapterform': chapterform, 'success': False}, request))

    def total_chapters(self,mangaseries):
        chapters = Chapter.objects.filter(manga=mangaseries)
        return len(chapters)        

class NewOneShotFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/new_oneshot_form.html'
    def get(self, request, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        if existing_creator is not None:
            oneshotform = OneShotForm()
            template = loader.get_template('accounts/new_oneshot_form.html')
            return HttpResponse(template.render({'oneshotform': oneshotform}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self, request, *args, **kwargs):
        oneshotform = OneShotForm(request.POST,request.FILES or None)
        images = request.FILES.getlist('images')
        print(request.POST, flush=True)
        template = loader.get_template('accounts/new_oneshot_form.html')
        if oneshotform.is_valid():
            creator = Creator.objects.filter(user=request.user).first()
            title = bleach.clean(oneshotform.cleaned_data['title'])
            cover_picture = oneshotform.cleaned_data['cover_picture']
            plot = bleach.clean(oneshotform.cleaned_data['plot'])
            primary_Genre = bleach.clean(oneshotform.cleaned_data['primary_Genre'])
            secondary_Genre = bleach.clean(oneshotform.cleaned_data['secondary_Genre'])
            if(primary_Genre == 'Select' or secondary_Genre == 'Select'):
                print('invalid_genre', flush=True)
                return HttpResponse(template.render({'oneshotform': oneshotform, 'success': False, 'invalid_genre': True}, request))
            oneshot = OneShot.objects.create(creator=creator,title=title,cover_picture=cover_picture,plot=plot,primary_Genre=primary_Genre,secondary_Genre=secondary_Genre)
            oneshot.save()
            print(oneshot, flush=True) 
            no = 1
            for image in images:
                print(image, flush=True)
                oneshotimage = OneShotImages.objects.create(oneshot=oneshot,image=image,no=no)
                no += 1

            return HttpResponseRedirect("/accounts/profile")
        else:
            print('Form invalid', flush = True)
            return HttpResponse(template.render({'oneshotform': oneshotform, 'success': False}, request))

class EditMangaFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/edit_manga_form.html'
    def get(self, request, pk, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        manga = MangaSeries.objects.filter(pk=pk).first() 
        cover_picture = manga.cover_picture
        print(manga , flush=True)
        if existing_creator is not None and manga.creator == existing_creator:
            form=EditMangaForm(initial={'title':manga.title, 'primary_Genre': manga.primary_Genre, 'secondary_Genre': manga.secondary_Genre, 'plot': manga.plot})
            template = loader.get_template('accounts/edit_manga_form.html')
            return HttpResponse(template.render({'form': form, 'cover_picture': cover_picture}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self, request,pk, *args, **kwargs):
        template = loader.get_template('accounts/edit_manga_form.html')
        manga = MangaSeries.objects.filter(pk=pk).first()
        cover_picture = manga.cover_picture
        if request.POST.get('title') == manga.title:
            post = request.POST.copy()
            post['title']=''
        form = EditMangaForm(post,request.FILES or None)
        if form.is_valid():
            creator = Creator.objects.filter(user=request.user).first()
            if(bleach.clean(form.cleaned_data['primary_Genre']) == 'Select' or  bleach.clean(form.cleaned_data['secondary_Genre']) == 'Select'):
                print('invalid_genre', flush=True)
                form = EditMangaForm(request.POST,request.FILES or None)
                return HttpResponse(template.render({'form': form, 'cover_picture': cover_picture, 'success': False, 'invalid_genre': True}, request))
            if form.cleaned_data['title'] != '': 
                manga.title = form.cleaned_data['title']
            if form.cleaned_data['cover_picture'] != None:
                manga.cover_picture = form.cleaned_data['cover_picture']
            manga.plot = bleach.clean(form.cleaned_data['plot'])
            manga.primary_Genre = bleach.clean(form.cleaned_data['primary_Genre'])
            manga.secondary_Genre = bleach.clean(form.cleaned_data['secondary_Genre'])
            manga.save()
            return HttpResponseRedirect('/accounts/upload')
        else:
            print('Form invalid', flush = True)
            form = EditMangaForm(request.POST,request.FILES or None)
            return HttpResponse(template.render({'form': form, 'cover_picture': cover_picture, 'success': False}, request))

class EditChapterFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/edit_chapter_form.html'
    def get(self, request, pk, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        chapter = Chapter.objects.filter(pk=pk).first()
        chapterimages = ChapterImages.objects.filter(chapter=chapter).order_by('no')
        if existing_creator is not None and chapter.manga.creator == existing_creator:
            chapterform=ChapterForm(initial={"title":chapter.title})
            template = loader.get_template('accounts/edit_chapter_form.html')
            return HttpResponse(template.render({'chapterform': chapterform, 'chapterimages': chapterimages}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self,request,pk,*args,**kwargs):
        
        images = request.FILES.getlist('images')
        chapterform=ChapterForm(request.POST)
        template = loader.get_template('accounts/edit_chapter_form.html')   
        chapter = Chapter.objects.filter(pk=pk).first()
        if chapterform.is_valid():
            chapter.title = bleach.clean(chapterform.cleaned_data['title'])
            chapter.save()
            if images:
                no = 1
                chapterimages = ChapterImages.objects.filter(chapter=chapter).delete()
                for image in images:
                    print(image, flush=True)
                    chapterimage = ChapterImages.objects.create(chapter=chapter,image=image,no=no,views=chapter.views)
                    no += 1

            return HttpResponseRedirect("/accounts/profile")
        else:
            chapterimages = ChapterImages.objects.filter(chapter=chapter).order_by('no')
            print('Form invalid', flush = True)
            return HttpResponse(template.render({'chapterform': chapterform, 'chapterimages': chapterimages, 'success': False}, request))

class EditOneShotFormView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/edit_oneshot_form.html'
    def get(self, request, pk, *args, **kwargs):
        existing_creator = Creator.objects.filter(user=request.user).first()
        oneshot = OneShot.objects.filter(pk=pk).first() 
        cover_picture = oneshot.cover_picture
        oneshotimages = OneShotImages.objects.filter(oneshot=oneshot).order_by('no')
        print(oneshot , flush=True)
        if existing_creator is not None and oneshot.creator == existing_creator:
            oneshotform = EditOneShotForm(initial={'title':oneshot.title, 'primary_Genre': oneshot.primary_Genre, 'secondary_Genre': oneshot.secondary_Genre, 'plot': oneshot.plot})
            print(oneshotform, flush=True)
            template = loader.get_template('accounts/edit_oneshot_form.html')
            return HttpResponse(template.render({'oneshotform': oneshotform, 'cover_picture': cover_picture, "oneshotimages": oneshotimages}, request))
        else:
            return HttpResponseRedirect('/accounts/profile')

    def post(self, request,pk, *args, **kwargs):
        template = loader.get_template('accounts/edit_oneshot_form.html')
        oneshot = OneShot.objects.filter(pk=pk).first()
        cover_picture = oneshot.cover_picture
        images = request.FILES.getlist('images')
        oneshotimages = OneShotImages.objects.filter(oneshot=oneshot).order_by('no')
        if request.POST.get('title') == oneshot.title:
            post = request.POST.copy()
            post['title']=''
        oneshotform = EditOneShotForm(post,request.FILES or None)
        if oneshotform.is_valid():
            creator = Creator.objects.filter(user=request.user).first()
            if(bleach.clean(oneshotform.cleaned_data['primary_Genre']) == 'Select' or  bleach.clean(oneshotform.cleaned_data['secondary_Genre']) == 'Select'):
                print('invalid_genre', flush=True)
                oneshotform = EditOneShotForm(request.POST,request.FILES or None)
                return HttpResponse(template.render({'oneshotform': oneshotform, 'cover_picture': cover_picture, "oneshotimages": oneshotimages, 'success': False, 'invalid_genre': True}, request))
            if oneshotform.cleaned_data['title'] != '': 
                oneshot.title = oneshotform.cleaned_data['title']
            if oneshotform.cleaned_data['cover_picture'] != None:
                oneshot.cover_picture = oneshotform.cleaned_data['cover_picture']
            oneshot.plot = bleach.clean(oneshotform.cleaned_data['plot'])
            oneshot.primary_Genre = bleach.clean(oneshotform.cleaned_data['primary_Genre'])
            oneshot.secondary_Genre = bleach.clean(oneshotform.cleaned_data['secondary_Genre'])
           
            oneshot.save()
            if images:
                no = 1
                oneshotimages = OneShotImages.objects.filter(oneshot=oneshot).delete()
                for image in images:
                    print(image, flush=True)
                    oneshotimage = OneShotImages.objects.create(oneshot=oneshot,image=image,no=no)
                    no += 1

            return HttpResponseRedirect('/accounts/upload')
        else:
            print('Form invalid', flush = True)
            oneshotform = EditOneShotForm(request.POST,request.FILES or None)
            return HttpResponse(template.render({'oneshotform': oneshotform, 'cover_picture': cover_picture, "oneshotimages": oneshotimages, 'success': False}, request))

class BuyCoinsView(LoginRequiredMixin,TemplateView):
    template_name = 'accounts/buy_coins.html'
    def get(self,request,*args,**kwargs):
        coinoffers = CoinOffer.objects.all().order_by('pk') 
        awards = Award.objects.all().order_by('pk')  
        template = loader.get_template('accounts/buy_coins.html')
        return HttpResponse(template.render({'coinoffers':coinoffers, 'awards':awards, 'json_coinoffers':serializers.serialize('json', coinoffers)}, request))

def buy_coins(request,pk):
    if request.method == 'GET':
        if request.user.is_authenticated:
            coinoffers = CoinOffer.objects.all().order_by('pk') 
            awards = Award.objects.all().order_by('pk')  
            coinoffer = CoinOffer.objects.filter(pk=pk).first()
            template = loader.get_template('accounts/buy_coins.html')
            return HttpResponse(template.render({'coinoffers':coinoffers, 'awards':awards, 'coinoffer': coinoffer}, request))  

class WithdrawOrderInfo:
    def __init__(self, date, order):
        self.date = date
        self.order = order

class WithdrawOrderView(LoginRequiredMixin,TemplateView):
    template = 'accounts/withdraw_order.html'
    def get(self, request, *args, **kwargs):
        template = loader.get_template('accounts/withdraw_order.html')
        creator = request.user
        print(request.user.creator, flush=True)
        withdraw_orders = WithdrawOrder.objects.filter(creator=creator).order_by('-date_time')
        if withdraw_orders:
            withdraw_order_infos = [WithdrawOrderInfo(True, withdraw_orders[0])]
            for i in range(1,len(withdraw_orders)):
                print(withdraw_orders[i].date_time.strftime('%d.%m.%y'), flush = True)
                print(withdraw_orders[i-1].date_time.strftime('%d.%m.%y'), flush = True)
                if(withdraw_orders[i].date_time.strftime('%d.%m.%y') == withdraw_orders[i-1].date_time.strftime('%d.%m.%y')):
                    withdraw_order_infos.append(WithdrawOrderInfo(False, withdraw_orders[i]))
                else:
                    withdraw_order_infos.append(WithdrawOrderInfo(True, withdraw_orders[i]))
                print(len(withdraw_order_infos), flush=True)
        else:
            withdraw_order_infos = []
        return HttpResponse(template.render({'withdraw_order_infos':withdraw_order_infos}, request))

def process_order(request):
    print("I am processing the order", flush=True)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        price = data['order']['price']
        print('Price: ' + str(price), flush=True)
        amount = data['order']['amount']
        print('Coins: ' + str(amount), flush=True)
        coinoffer = CoinOffer.objects.filter(price=price, amount=amount).first()
        print(coinoffer,flush=True)
        if(coinoffer):
            coin_purchase_order = CoinPurchaseOrder.objects.create(user=request.user,price=price, amount=amount)
            coin_purchase_order.save()
            profile = Profile.objects.filter(user=request.user).first()
            profile.coins += amount
            profile.save()
    print('RELOAD',flush=True)
    return HttpResponseRedirect('/accounts/coins')

def get_data(request,*args,**kwargs):
    data = {
        'sales':100,
        'customers':10,
    }
    return JsonResponse(data)

def sign_up(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = SignUpForm()
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            #print(user.profile.birth_date, flush=True)
            user.profile.birth_date = form.cleaned_data['birth_date']
            user.profile.advertise = form.cleaned_data['advertise_consent']
            user.is_active = False
            print(user.is_active, flush=True)
            #user.profile.third_party_advertise = form.cleaned_data['third_party_advertise_consent']
            #user.profile.analytics = form.cleaned_data['analytics_consent']
            user.save()
            # password = form.cleaned_data['password1']
            # user = authenticate(username=user.username, password=password)
            # login(request, user)
            subject = 'Activate NetManga Account'
            email_template_name = 'accounts/activate_account_mail.html'
            if request.is_secure():
                protocol = 'https'
            else:
                protocol = 'http'
            parameters = {
                'email' : user.email,
                'user' : user,
                'domain' : f'{request.get_host()}',
                'site_name' : 'NetManga',
                'uid' : urlsafe_base64_encode((force_bytes(user.pk))),
                'token' : tokens.default_token_generator.make_token(user),
                'protocol' : protocol,
            }
            message = loader.render_to_string(email_template_name, parameters)
            html_message = strip_tags(message)
            try:
                send_mail(subject, html_message, '', [user.email], html_message=message, fail_silently=False)
            except:
                return HttpResponse('Invalid Header')

            return HttpResponseRedirect('/accounts/registration_done')
    else:
        raise NotImplementedError
    
    template = loader.get_template('accounts/signup.html')
    return HttpResponse(template.render({'form': form}, request))

def registration_done(request):
    template = loader.get_template('accounts/registration_done.html')
    return HttpResponse(template.render({}, request))

def activate_account(request,uidb64,token):
    # template = loader.get_template('accounts/login.html')
    print(uidb64, flush=True)
    user_pk = int(force_str(urlsafe_base64_decode(uidb64)))
    print(user_pk, flush=True)
    user = User.objects.filter(pk=user_pk).first()
    print(user.username, flush=True)
    print(user.is_active, flush=True)
    user.is_active = True
    user.save()
    print(user.is_active)
    print(token, flush=True)
    return HttpResponseRedirect('/accounts/login')


def log_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        form = LoginForm()
    elif request.method == 'POST':
        redirect_to = request.GET.get('next', '')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(redirect_to)
            else:
                user = User.objects.filter(username=username).first()
                print(user, flush=True)
                if not user.is_active:
                    error_message = 'This account has not been activated yet'
                else: 
                    error_message =  'Username or Password was incorrect'

                template = loader.get_template('accounts/login.html')
                return HttpResponse(template.render({'form': form, 'error_message': error_message}, request))
    else: 
        raise NotImplementedError
    
    template = loader.get_template('accounts/login.html')
    return HttpResponse(template.render({'form': form, 'success': True}, request))

def reset_password_request(request):
    # render_to_string() -> loader.render_to_string()
    # default_token_generator -> tokens.default_token_generator()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            print(user, flush=True)
            print(request.is_secure(), flush=True)
            if user:
                subject = 'Reset Password NetManga'
                email_template_name = 'accounts/reset_password_mail.html'
                if request.is_secure():
                    protocol = 'https'
                else:
                    protocol = 'http'
                parameters = {
                    'email' : email,
                    'user' : user,
                    'domain' : f'{request.get_host()}',
                    'site_name' : 'NetManga',
                    'uid' : urlsafe_base64_encode((force_bytes(user.pk))),
                    'token' : tokens.default_token_generator.make_token(user),
                    'protocol' : protocol,
                }
                message = loader.render_to_string(email_template_name, parameters)
                html_message = strip_tags(message)
                try:
                    send_mail(subject, html_message, '', [email], html_message=message, fail_silently=False)
                except:
                    return HttpResponse('Invalid Header')
                return redirect('password_reset_done')

    else:
        form = ResetPasswordForm()
    template = loader.get_template('accounts/password_reset.html')
    return HttpResponse(template.render({'form': form}, request))
