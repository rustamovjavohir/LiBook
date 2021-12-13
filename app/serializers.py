from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializers(ModelSerializer):
    class Meta:
        model = Users
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
