from django.db.models import Count

from blog.models import SocialMedia,Article,Category

def socialMedia(request):
    socialMedias = SocialMedia.objects.all()
    return {'socialMedia' : socialMedias}

def recent_articles(request):
    recent_article = Article.objects.all().order_by("-created")[:3]
    return {'recent_articles':recent_article}

def category_list(request):
    categorys = Category.objects.all()
    return {'category':categorys}

def most_liked_articles(request):
    most_liked_article = Article.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:5]
    return {'most_liked_articles':most_liked_article}

