from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    img_url = models.CharField(blank=True, max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"

class Post(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_postings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    initial_p = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.item} auction by {self.seller}"

    # Make sure that one item only has one posting and vice versa
    class Meta:
        unique_together = ('item',)

class Bid(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_posts")
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.amount} gold - {self.bidder}"

class Comment(models.Model):
    posting = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_posts")
    content = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.user}: {self.content}"

class Category(models.Model):
    cat_name = models.CharField(max_length=64)
    cat_description = models.CharField(max_length=500)
    cat_items = models.ManyToManyField(Item, blank=True, related_name="categories")

    # Changes plural form in admin page (Default is categorys)
    class Meta:
        verbose_name_plural = "categories"