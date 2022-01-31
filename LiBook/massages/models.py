from datetime import datetime

from django.db import models

# Create your models here.
from app.models import Book, User


class Like(models.Model):
    book_file = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        try:
            return "%s - %s" % (self.user.username, self.likes)
        except Exception as e:
            print(e)
            return ""


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    modifaty_time = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.message[:10]

    @property
    def update_date(self):
        self.modifaty_date = datetime.now()
        self.save()
        return self


class ReplyMessage(models.Model):
    basic_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.user.username, self.message[:10])
