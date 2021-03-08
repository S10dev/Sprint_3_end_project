from django.contrib import admin

from .models import Post, Group, Disk, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group", 'image') 
    search_fields = ("text",) 
    list_filter = ("pub_date",) 
    empty_value_display = "-пусто-"
# это свойство сработает для всех колонок: где пусто - там будет эта строка

class GroupAdmin(admin.ModelAdmin):
    list_display = ("slug","title","description") 
    search_fields = ("title",)
    list_filter = ("title",) 
    empty_value_display = "-пусто-"


class DiskAdmin(admin.ModelAdmin):
    list_display = ("pk", "artist", 'new_request', 'date')
    search_fields = ("artist",) 
    list_filter = ("artist",) 
    empty_value_display = "-пусто-"


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("author", "post", 'text')
    search_fields = ("author",) 
    list_filter = ("author",) 
    empty_value_display = "-пусто-"    



class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user")
    search_fields = ("author",) 
    list_filter = ("author",) 
    empty_value_display = "-пусто-"  


# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(Disk, DiskAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Follow, FollowAdmin)