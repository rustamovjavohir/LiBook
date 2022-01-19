from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class UserSerializers(ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    date_of_birth = serializers.DateField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name',"email",'date_of_birth','password') # 'password'

# class AkkountSerializers(ModelSerializer):
#     class Meta:
#         model = Akkount
#         fields = "__all__"

class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BookSerializers(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BoxSerializers(ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"

class MessageSerializers(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ReplyMessageSerializers(ModelSerializer):
    class Meta:
        model = ReplyMessage
        fields = "__all__"

class AdviceSerializers(ModelSerializer):
    class Meta:
        model = Advice
        fields = "__all__"
