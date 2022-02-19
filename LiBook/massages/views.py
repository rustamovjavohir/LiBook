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

    @action(methods=['post'], detail=False, url_path='hello', url_name='hello')
    def hello(self, request):
        return Response({"hello": f" {request.data['name']} Hello"})

    @action(methods=['post'], detail=True, url_path='detail2', url_name='detail2')
    def detail2(self, request, **kwargs):
        return Response({"hello": f" {request.data['name']} Hello with detail2"})

    def retrieve(self, request, *args, **kwargs):
        response = Response()
        m_id = int(kwargs['pk'])
        message = get_object_or_404(klass=Message, id=int(m_id))
        message_serializer = MessageSerializers(message)
        data = message_serializer.data
        rep_message = ReplyMessage.objects.filter(basic_message=m_id)
        rep_mes_ser = ReplyMessageSerializers(rep_message, many=True)
        data["replay_message"] = rep_mes_ser.data
        response.data = data
        return response




class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers
