from .models import Profile, Creator, MangaSeries, Chapter, ChapterImages, Subscriber, ChapterRating, ChapterComment, ChapterCommentRating

class MangaInfo:
    def __init__(self,manga,latest_chapter):
        self.manga = manga
        self.latest_chapter = latest_chapter

def mergeSort_by_latest_upload(list):
    if len(list) > 1:
        mid = len(list)//2
        left = list[:mid]
        right = list[mid:]
        mergeSort_by_latest_upload(left)
        mergeSort_by_latest_upload(right)

        i = j = k = 0

        while i < len(left) and j  < len(right):
            if left[i].latest_chapter.published > right[j].latest_chapter.published:
                list[k] = left[i]
                i+=1
            else:
                list[k] = right[j]
                j+=1
            k+=1

        while i < len(left):
            list[k] = left[i]
            i+=1
            k+=1

        while j < len(right):
            list[k] = right[j]
            j+=1
            k+=1

class Tuple:
    def __init__(self,manga):
        self.manga = manga
        self.views = 0

    def add_views(self,views):
        self.views += views 

    def __str__(self):
        if self.manga:
            print('Manga: ' + str(self.manga.title) + '\nViews: ' + str(self.views))
        else:
            print('None')

def sort_view(creator):
    mangaseries = MangaSeries.objects.filter(creator=creator)
    sorted_list = []
    for manga in mangaseries:
        chapters = Chapter.objects.filter(manga=manga)
        view_tuple = Tuple(manga)
        for chapter in chapters:
            view_tuple.add_views(chapter.views)
            
        sorted_list.append(view_tuple)
        mergeSort_by_total_views(sorted_list)    
    return sorted_list
    

def mergeSort_by_total_views(list):
    if len(list) > 1:
        mid = len(list)//2
        left = list[:mid]
        right = list[mid:]
        mergeSort_by_total_views(left)
        mergeSort_by_total_views(right)

        i = j = k = 0

        while i < len(left) and j  < len(right):
            if left[i].views > right[j].views:
                list[k] = left[i]
                i+=1
            else:
                list[k] = right[j]
                j+=1
            k+=1

        while i < len(left):
            list[k] = left[i]
            i+=1
            k+=1

        while j < len(right):
            list[k] = right[j]
            j+=1
            k+=1