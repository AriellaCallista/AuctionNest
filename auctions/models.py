from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=100)
    photo_url = models.TextField(default=None) # sets default value of url to None if not filled
    category = models.CharField(max_length=64, default=None)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    isActive = models.BooleanField(default=True)
    watchlisted_by = models.ManyToManyField(User, blank=True, related_name="watchlist")
    startingBid = models.FloatField(default=0)
    highestBid = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")

    def save(self, *args, **kwargs):
        if self.highestBid is None:
            self.highestBid = self.startingBid
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} /n {self.desc}"



class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    created_at = models.TimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"


