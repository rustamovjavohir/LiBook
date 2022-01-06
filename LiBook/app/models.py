from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Akkount(models.Model):
    # name = models.CharField(max_length=35,null=True,blank=True)
    # username = models.CharField(max_length=35,unique=True)
    # gmail = models.EmailField(null=True,blank=True,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    photo = models.ImageField(null=True,blank=True)
    @property
    def full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField("Kategoriya name",max_length=100, null=True)
    photo = models.ImageField(null=True,blank=True)
    views = models.IntegerField(default=0)
    status = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
        try:
            return self.name
        except Exception as e:
            return ""
class Book(models.Model):
    TYPE = (('AUDIO',"AUDIO"),
            ("DOC","DOC"))
    LANG = (('UZ',"UZ"),
            ("RU","RU"))
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    author = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    about = models.TextField(null=True)
    file = models.FileField(null=True)
    add_date = models.DateField(auto_now_add=True,blank=True)
    photo = models.ImageField(null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    type = models.CharField(max_length=6,null=True,choices=TYPE,default="DOC")
    lang = models.CharField(max_length=2,null=True,default="UZ",choices=LANG)
    views = models.IntegerField(default=0)


    # @property
    def __str__(self):
        return self.name

class Like(models.Model):
    book_file = models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(Akkount,on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        try:
            return "%s - %s" % (self.user.username,self.likes)
        except Exception as e:
            print(e)
            return ""

class Box(models.Model):
    user = models.ForeignKey(Akkount,on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.book.name


class Message(models.Model):
    user = models.ForeignKey(Akkount,on_delete=models.CASCADE,null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True,blank=True)
    modifaty_time = models.DateTimeField(null=True,blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.message[:10]

    @property
    def update_date(self):
        self.modifaty_date = datetime.now()
        self.save()
        return self


class ReplyMessage(models.Model):
    basic_message = models.ForeignKey(Message,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(Akkount,on_delete=models.CASCADE,null=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return "%s %s" % (self.user.username,self.message[:10])