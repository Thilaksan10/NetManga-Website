from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone
from decimal import Decimal

from .choices import GENRE_CHOICES, STATUS_CHOICES

# Create your models here.
class Profile(models.Model):
    #owner
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(default="static/static/vol/web/media/img/no_profile_picture.png", null=True, blank=True, upload_to='profilepictures/')
    is_full_name_displayed = models.BooleanField(default=True)

    # details
    bio = models.CharField(max_length=500, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    advertise = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)

@receiver(post_save,sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

    instance.profile.save()

class Creator(models.Model):
    #owner
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='creator', null=True) 
    is_profile_picture_displayed = models.BooleanField(default=True)
    
    #details
    mangas_published = models.IntegerField(default=0) 
    chapters_published = models.IntegerField(default=0)
    total_readers = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    subscribers = models.IntegerField(default=0)
    earned_money = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=Decimal(0.00))

class Mangaseries(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE,blank=True,null=True)

    title = models.CharField(unique=True,max_length=100)
    cover_picture = models.ImageField(blank=True, upload_to='coverpictures/')
    plot = models.CharField(max_length=1000)
    primary_Genre = models.CharField(max_length=18,choices=GENRE_CHOICES, blank=True, null=True)
    secondary_Genre = models.CharField(max_length=18,choices=GENRE_CHOICES, blank=True, null=True)

class Chapter(models.Model):
    manga = models.ForeignKey(Mangaseries, on_delete=models.CASCADE)
    
    published = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100)
    no = models.IntegerField(null=True)
    views = models.IntegerField(default=0)
    
class Subscriber(models.Model):
    manga = models.ForeignKey(Mangaseries, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

class Rating(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.BooleanField(null=True)

class Comment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    comment = models.CharField(max_length=500)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)

class CommentRating(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.BooleanField(null=True)

def get_image_filename(instance, filename):
    manga = instance.chapter.manga.title
    title = instance.chapter.title
    slug_manga = slugify(manga)
    slug_title = slugify(title)
    return 'chapter_images/%s/%s/%s' % (slug_manga,slug_title, filename)

class Chapterimages(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, max_length=1000, upload_to=get_image_filename)
    no = models.IntegerField(null=True)
    views = models.IntegerField(default=0)

class CoinOffer(models.Model):
    amount = models.IntegerField(default=0)
    price = models.FloatField(default=float(0.00))
    bonus = models.IntegerField(default=0)

class Award(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to='awards/')
    price = models.IntegerField(default=0)
    fiat_reward = models.FloatField(default=float(0.00))
    coins_reward = models.IntegerField(default=0)
    
class ChapterAward(models.Model):
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

class ReportChapter(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.CharField(max_length=1000)    
    
class CoinPurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField(default=float(0.00))
    amount = models.IntegerField(default=0)
    date_time = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)

class WithdrawOrder(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    paypal = models.CharField(null=False, max_length=10000)
    amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, null=False,max_length=10)


'''
class Manga(models.Model):
    GENRE_CHOICES = (
        ('Action','Action'),
        ('Drama','Drama'),
        ('Comedy','Comedy'),
        ('Fantasy','Fantasy'),
        ('Slice of Life', 'Slice of Life'),
        ('Romance', 'Romance'),
        ('Superhero','Superhero'),
        ('Sci-Fi','Sci-Fi'),
        ('Thriller','Thriller'),
        ('Supernatural','Supernatural'),
        ('Mystery','Mystery'),
        ('Sports','Sports'),
        ('Historical','Historical'),
        ('Heartwarming','Heartwarming'),
        ('Horror','Horror'),
        ('Informative','Informative'),
    )

    #creator
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)

    #details
    name = models.CharField(max_length=100, blank=True, unique=True)
    cover_picture = models.ImageField(blank=True)
    manga_started = models.DateField(blank=True, null=True)
    published_chapters = models.IntegerField(blank = True , null=True)
    primary_genre = models.CharField(max_length=15,choices=GENRE_CHOICES, blank=True, null=True)
    secondary_genre = models.CharField(max_length=15,choices=GENRE_CHOICES, blank=True, null=True)
    tertiary_genre = models.CharField(max_length=15,choices=GENRE_CHOICES, blank=True, null=True)
    readers = models.IntegerField(blank = True , null=True)
    likes = models.IntegerField(blank = True , null=True)
    dislikes = models.IntegerField(blank = True , null=True)
    subscribers = models.IntegerField(blank = True , null=True)
'''    











''' 
class Manga(models.Model):
    #creator
    user = model.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    #details
    name = models.CharField(max_length=100, blank=True, null=True)
    series_started = models.DateField(blank=True,null=True)
    chapters_released = models.
''' 