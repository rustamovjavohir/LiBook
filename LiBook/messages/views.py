from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Message, ReplyMessage
from .serializers import MessageSerializers, ReplyMessageSerializers


class MessageViews(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

    def retrieve(self, request, *args, **kwargs):
        response = Response()
        m_id = kwargs['pk']
        data = []
        message = get_object_or_404(klass=Message, id=int(m_id))
        message_serializer = MessageSerializers(message)
        data = dict(message_serializer.data)
        data["detail"] = "success"
        response.data = data
        return response


class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers
