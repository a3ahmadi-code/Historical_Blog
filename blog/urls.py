from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.HomeView, name="home"),
    path('article/list', views.ArticleListListView.as_view(), name="article_list"),
    path('contact', views.ContactUsCreateView.as_view(), name="contact"),
    path('about', views.AboutTemplateView.as_view(), name="about"),
    path('category/detail/<int:pk>', views.category_detail, name="category_detail"),
    path('article/detail/<slug:slug>', views.ArticleDetailVeiw.as_view(), name="article_detail"),
    path('search/', views.search_Veiw, name="search"),
    path('like/<slug:slug>/<int:pk>', views.like, name="like"),
]
