from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','password','username','first_name','last_name',"email")

class AkkountSerializers(ModelSerializer):
    class Meta:
        model = Akkount
        fields = "__all__"

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
