from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from massages.models import Message, ReplyMessage
from massages.serializers import MessageSerializers, ReplyMessageSerializers


class MessageViews(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

    def retrieve(self, request, *args, **kwargs):
        response = Response()
        m_id = int(kwargs['pk'])
        message = get_object_or_404(klass=Message, id=int(m_id))
        message_serializer = MessageSerializers(message)
        data = dict(message_serializer.data)
        rep_message = ReplyMessage.objects.filter(basic_message=m_id)
        rep_mes_ser = ReplyMessageSerializers(rep_message, many=True)
        data["replay_message"] = rep_mes_ser.data
        response.data = data
        return response

    @action(methods=['post'], detail=True, url_path='hello', url_name='hello')
    def hello(self, request, pk=None):
        return Response({"hello": f"{pk} {request.data['name']} Hello"})


class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers
