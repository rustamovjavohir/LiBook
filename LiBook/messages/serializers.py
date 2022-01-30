from rest_framework.serializers import ModelSerializer

from .models import Message, ReplyMessage


class MessageSerializers(ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"


class ReplyMessageSerializers(ModelSerializer):
    class Meta:
        model = ReplyMessage
        fields = "__all__"
