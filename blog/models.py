from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category (models.Model):
    title = models.CharField(max_length=200,verbose_name="عنوان")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    class Meta:
        ordering = ('-created_at',)
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Article (models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="نویسنده")
    category = models.ManyToManyField(Category,verbose_name="دسته بندی",related_name='articles')
    title = models.CharField(max_length=200,verbose_name="عنوان")
    body = models.TextField(verbose_name="متن")
    image = models.ImageField(upload_to="article",verbose_name="تصویر")
    published = models.BooleanField(default=False,verbose_name="تاییدیه پخش")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.slug = slugify(self.title)
        super(Article,self).save()

    def __str__(self):
        return f"{self.author} - {self.title} - {self.published}"

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})



    class Meta:
        ordering = ('-created',)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"


class Comment (models.Model):
    objects = None
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name="مقاله",related_name="comments")
    user = models.ForeignKey(User,verbose_name="کاربر",related_name="commentse",on_delete=models.CASCADE)
    prent = models.ForeignKey('self',on_delete=models.CASCADE,related_name="repli",blank=True,null=True,verbose_name="پاسخ")
    body = models.TextField(verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:20]

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"


class ContactUs (models.Model):
    user = models.ForeignKey(User,related_name="contacts",verbose_name="کاربر",on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    body = models.TextField(verbose_name="Text")

    def __str__(self):
        return f"{self.user} - {self.subject} - {self.body}"

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"


class SocialMedia(models.Model):
    objects = None
    Facebook = models.URLField()
    Twitter = models.URLField()
    Telegram = models.URLField()
    Tel = models.CharField(max_length=20)
    Email = models.EmailField()
    Address = models.TextField()

    class Meta:
        verbose_name = "رسانه اجتماعی"
        verbose_name_plural = "رسانه های اجتماعی"


class AboutDynamic(models.Model):
    Description = models.TextField()
    More_details1 = models.TextField()
    More_details2 = models.TextField()
    More_details3 = models.TextField()
    More_details4 = models.TextField()
    More_details5 = models.TextField()
    image = models.ImageField(upload_to="AboutDynamic_image")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "اطلاعات متغیر صفحه about"
        verbose_name_plural = "اطلاعات های متغیر صفحه about"


class Like (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="like",verbose_name='کاربر')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="likes",verbose_name='مقاله')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.article}'

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"
        ordering = ["created_at"]



