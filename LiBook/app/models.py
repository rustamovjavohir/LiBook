from django.db import models
from django.contrib.auth.models import User

class Users(models.Model):
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


class Book(models.Model):
    TYPE = (('AUDIO',"AUDIO"),
            ("DOC","DOC"))
    LANG = (('UZ',"UZ"),
            ("RU","RU"))
    author = models.CharField(max_length=100,null=True)
    name = models.CharField(max_length=100,null=True)
    about = models.TextField(null=True)
    file = models.FileField(null=True)
    add_date = models.DateField(auto_now_add=True,blank=True)
    photo = models.ImageField(null=True,blank=True)
    status = models.IntegerField(null=True,blank=True)
    type = models.CharField(max_length=6,null=True,choices=TYPE,default="DOC")
    lang = models.CharField(max_length=2,null=True,default="UZ",choices=LANG)

    # @property
    def __str__(self):
        return self.name


class Box(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.book.name



class Message(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.message[:10]
