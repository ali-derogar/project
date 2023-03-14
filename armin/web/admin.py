from csv import list_dialects
import ipaddress
from django.contrib import admin
from .models import Article , Category , S_title , Ipaddress , Introduce , Slideshow , Email_Saver

admin.site.site_header = 'پنل مدیریتی'

def make_publish(modeladmin , request , queryset):
    row = queryset.update(status = 'p')
    modeladmin.message_user(request , ' تعداد مقاله های منتشر شده {}'.format(row))
make_publish.short_description = 'انتشار مقالات انتخاب شده'

def make_special(modeladmin , request , queryset):
    row = queryset.update(is_special = True)
    modeladmin.message_user(request , ' تعداد مقاله های ویژه {}'.format(row))
make_special.short_description = 'ویژه شدن مقالات انتخاب شده'

def make_draft(modeladmin , request , queryset):
    row = queryset.update(status = 'd')
    modeladmin.message_user(request , ' تعداد مقاله های تعلیق شده {}'.format(row))
make_draft.short_description = 'تعلیق مقالات انتخاب شده'



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title' ,'slug' ,'jpublish','is_special','thumbnail_tag' ,'status','category_to_str')
    search_fields = ('title' , 'descriptions')
    list_filter = ('status' ,'is_special', 'published')
    prepopulated_fields = {'slug' : ('title',)}
    ordering = ('status' ,'published')
    actions = [make_publish , make_draft, make_special]
admin.site.register(Article , ArticleAdmin)

class SlideshowAdmin(admin.ModelAdmin):
    list_display = ('name' ,'detail')
    search_fields = ('name' ,)
admin.site.register(Slideshow , SlideshowAdmin)

class Email_SaverAdmin(admin.ModelAdmin):
    list_display = ('created' ,'email')
    search_fields = ('email' ,'created')
admin.site.register(Email_Saver , Email_SaverAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title' ,'position' , 'slug' ,'status','parent')
    search_fields = ('title',)
    list_filter = ('status' ,)
    prepopulated_fields = {'slug' : ('title',)}
admin.site.register(Category , CategoryAdmin)

class Site_titleAdmin(admin.ModelAdmin):
    list_display = ('position' , 'title' ,'slug' ,'status')
    search_fields = ('title',)
    list_filter = ('status' , 'position')
    prepopulated_fields = {'slug' : ('title',)}
admin.site.register(S_title , Site_titleAdmin)
admin.site.register(Ipaddress)

class IntroduceAdmin(admin.ModelAdmin):
    list_display = ('name' ,"number",'about' ,'slug','pic_tag')
    search_fields = ('name' ,'about')
    list_filter = ('name',)
admin.site.register(Introduce , IntroduceAdmin)
