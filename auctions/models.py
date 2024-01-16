from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    cat_name = models.CharField(max_length=64)
    cat_description = models.CharField(max_length=500)

    # Changes plural form in admin page (Default is categorys)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return f"{self.cat_name}"

class Item(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    img_url = models.CharField(blank=True, max_length=100)
    categories = models.ManyToManyField(Category, blank=True, related_name="items")

    def __str__(self) -> str:
        return f"{self.name}"

class Post(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_postings")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    initial_p = models.IntegerField()
    post_datetime = models.DateTimeField()
    watched_by = models.ManyToManyField(User, blank=True, related_name="watchlist")
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="wins")

    def __str__(self) -> str:
        return f"{self.item} auction by {self.seller}"

    # Make sure that one item only has one posting and vice versa
    class Meta:
        unique_together = ('item',)

class Bid(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_posts")
    amount = models.IntegerField()
    bid_datetime = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.amount} gold - {self.bidder}"
    
    # Alter default Bid.save() behaviour
    def save(self, *args, **kwargs):
        # Get last bid on same post
        last_bid = Bid.objects.filter(post=self.post).order_by('-bid_datetime').first()

        if last_bid and self.amount <= last_bid.amount:
            raise ValidationError("New bid amount must be higher than the last bid.")

        super().save(*args, **kwargs)

class Comment(models.Model):
    posting = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_posts")
    content = models.CharField(max_length=200)
    comment_datetime = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.user}: {self.content}"

