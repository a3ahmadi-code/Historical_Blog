from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import TemplateView,ListView,DetailView,CreateView
from .models import Article,Category,AboutDynamic,ContactUs,Comment,Like
from django.db.models import Q, Count


def HomeView(request):

    article2 = Article.objects.all().order_by("created")[:3]
    article1 = Article.objects.filter(published=True)

    # مقالات پرلایک رو می‌گیریم
    most_liked_articles = Article.objects.annotate(
        like_count=Count('likes')
    ).order_by('-like_count')[:5]  # فقط ۵ مقاله اول

    return render(request,"blog/home.html",{'article2' : article2 ,'article1':article1,'most_liked_articles':most_liked_articles})


class AboutTemplateView(TemplateView):
    template_name = "blog/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['AboutDynamic'] = AboutDynamic.objects.all()
        return context


class ContactUsCreateView(CreateView):
    template_name = "blog/contact.html"
    success_url = "/"
    model = ContactUs
    fields = ["subject","body"]

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)


class ArticleListListView(ListView):
    # queryset = Article.objects.filter(published=True)
    paginate_by = 1
    model = Article
    template_name = "blog/article_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        most_liked_article = Article.objects.annotate(
            like_count=Count('likes')
        ).order_by('-like_count')[:5]
        context['most_liked_articles'] = most_liked_article
        return context

def category_detail(request,pk):
    category = get_object_or_404(Category,id=pk)
    categorys = category.articles.all()
    return render(request,"blog/article_list.html",{'object_list':categorys})


class ArticleDetailVeiw(DetailView):
    model = Article
    template_name = "blog/article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # گرفتن مقاله بر اساس slug
        body = request.POST.get('body')
        pr_id = request.POST.get('pr_id')

        Comment.objects.create(
            body = body,
            article = self.object,
            prent_id = pr_id,
            user = request.user
        )

        return redirect(f'/article/detail/{self.object.slug}' + '#col-lg-12')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        comments = Comment.objects.filter(article=self.object,prent__isnull=True).order_by('-created_at')
        paginator = Paginator(comments,1)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['com'] = page_obj
        ###
        if self.request.user.is_authenticated:
            if self.request.user.like.filter(article__slug=self.object.slug,user_id=self.request.user.id).exists():
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        ###
        return context

def search_Veiw(request):
    q = request.GET.get('q')
    result_search = Article.objects.filter(Q(body__icontains=q) | Q(title__icontains=q))
    return render(request,'blog/article_list.html',{'object_list': result_search})


def like(request,slug,pk):
    if not request.user.is_authenticated:
        return redirect('account:login')
    try:
        liked = Like.objects.get(article__slug=slug,user_id=request.user.id)
        liked.delete()
        return JsonResponse({'response': 'unliked'})
    except:
        Like.objects.create(article_id=pk,user_id=request.user.id)
        return JsonResponse({'response':'liked'})


