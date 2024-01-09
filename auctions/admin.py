from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Bid, Category, Comment, Item, Post, User

# Register your models here.
class BidAdmin(admin.ModelAdmin):
    list_display = ("post", "bidder", "amount",)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("cat_name", "cat_description")

    filter_horizontal = ("cat_items",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("posting", "user", "content")

class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "img_url",)

class PostAdmin(admin.ModelAdmin):
    list_display = ("item", "seller",)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "first_name", "last_name", "is_staff",)

admin.site.register(Bid, BidAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, CustomUserAdmin)
