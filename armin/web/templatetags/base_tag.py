from django import template
from ..models import Article, S_title , Category
from django.db.models import Count , Q
from datetime import datetime , timedelta
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('web/partial/nav_bar.html')
def nav_barr():
    return {
        'category' : Category.objects.filter(status = True),
        'title' : S_title.objects.get(position = 1)
    }

@register.inclusion_tag('web/partial/sidebar.html')
def popular_article():
    last_month = datetime.today() - timedelta(days=30)
    return {
        'article' : Article.objects.publish().annotate(count=Count("hits",filter=Q(articlehit__created__gt=last_month))).order_by("-count","-published")[:5],
        "title" : "مقالات پر بازدید ماه",
        "hot" : "بیشترین بازید"
    }

@register.inclusion_tag('web/partial/sidebar.html')
def hot_article():
    last_month = datetime.today() - timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='web', model='article').id
    return {
        'article' : Article.objects.publish().annotate(count=Count("comments",filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))).order_by("-count","-published")[:5],
        "title" : "مقالات داغ ماه",
        "hot" : "بیشترین کامنت"
    }