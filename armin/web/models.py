from ipaddress import ip_address
from operator import truediv
from accont.models import User
from django.utils.html import format_html
from django.db import models
from django.utils import timezone
from extentions.utils import time_convertor
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


#                      class mangers
class Article_activate(models.Manager):
    def publish(self):
        return self.filter(status="p")


class Category_activate(models.Manager):
    def active(self):
        return self.filter(status=True)
#                      models


class Ipaddress(models.Model):

    ipaddress = models.GenericIPAddressField(verbose_name="آدرس ای پی")

    class Meta:
        verbose_name = 'ای پی '
        verbose_name_plural = ' ای پی ها'

    def __str__(self):
        return self.ipaddress


class Category(models.Model):

    title = models.CharField(max_length=50, verbose_name='عنوان')
    position = models.IntegerField(unique=True, verbose_name='جایگاه')
    parent = models.ForeignKey('self', default=None, null=True, blank=True,
                               on_delete=models.SET_NULL, verbose_name='دسته اصلی', related_name='child')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='لینک')
    status = models.BooleanField(default=True, verbose_name='وضعیت انتشار')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['parent_id', 'position']

    objects = Category_activate()

    def __str__(self):
        return self.title


class Slideshow(models.Model):
    name = models.CharField(max_length=50, verbose_name="نام تصویر")
    detail = models.TextField(blank=True, verbose_name="توضیحات تصویر")
    image = models.ImageField(upload_to='images', verbose_name="انتخاب تصویر")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"


class Article(models.Model):

    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشر شود'),
        ('i', 'درحال بررسی'),
        ('b', 'بازگشت داده شود')
    )

    title = models.CharField(max_length=50, verbose_name='عنوان')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                            verbose_name='نویسنده', related_name='article')
    slide = models.ManyToManyField(
        Slideshow, blank=True, verbose_name="گالری", related_name="article")
    descriptions = models.TextField(verbose_name='توضیحات')
    is_special = models.BooleanField(
        default=False, verbose_name='ویژه بودن مقاله')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='لینک')
    category = models.ManyToManyField(
        'Category', verbose_name='دسته بندی', related_name='article_category')
    thumbnail = models.ImageField(upload_to='images', verbose_name='عکس')
    published = models.DateTimeField(
        default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    update = models.DateTimeField(auto_now=True, verbose_name='زمان آبدیت')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت انتشار')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(Ipaddress, through="Articlehit",
                                blank=True, verbose_name="آدرس ای پی", related_name="hits")

    def category_to_str(self):
        return '/'.join([i.title for i in self.category.filter(status=True)])
    category_to_str.short_description = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('account:home')

    def jpublish(self):
        return time_convertor(self.published)

    def thumbnail_tag(self):
        return format_html("<img style='width: 160px;height: 110px; border:1px solid pink;border-radius:15px 0 15px 0' src={}>".format(self.thumbnail.url))

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    objects = Article_activate()

    def __str__(self):
        return self.title


class S_title(models.Model):

    title = models.CharField(max_length=15, verbose_name='عنوان سایت')
    slug = models.SlugField(unique=True, verbose_name='لینک')
    position = models.IntegerField(unique=True, verbose_name='جایگاه')
    status = models.BooleanField(default=False, verbose_name='وضعیت')

    class Meta:
        verbose_name = 'عنوان سایت'
        verbose_name_plural = 'عنواین برای سایت'
        ordering = ['position']

    def __str__(self):
        return self.title


class Articlehit(models.Model):

    ip_address = models.ForeignKey(Ipaddress, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')


class Introduce(models.Model):
    name = models.CharField(max_length=100, verbose_name="نوع مهارت")
    pic = models.ImageField(upload_to="media", verbose_name="تصویر")
    about = models.TextField(verbose_name="درباره مهارت")
    slug = models.SlugField(unique=True, verbose_name='لینک')
    number = models.IntegerField(
        unique=False, verbose_name="درصد تسلط بر مهارت")

    def pic_tag(self):
        return format_html("<img style='width: 160px;height: 110px; border:1px solid pink;border-radius:15px 0 15px 0' src={}>".format(self.pic.url))

    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت ها"


class Email_Saver(models.Model):
    email = models.EmailField(max_length=254, verbose_name='ایمیل کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    
    def get_absolute_url(self):
        return reverse('web:home')

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = "ایمیل"
        verbose_name_plural = "ایمیل ها"