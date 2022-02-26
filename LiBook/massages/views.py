from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

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

    @swagger_auto_schema(operation_summary="Id orqali messagelarni chop etish")
    def retrieve(self, request, *args, **kwargs):
        """
        Id orqali messagelarni chop etish
        """
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

    @swagger_auto_schema(operation_summary="Messagelar ro`yhatini chop etish")
    def list(self, request, *args, **kwargs):
        """
        Messagelar ro`yhatini chop etish
        """
        return super(MessageViews, self).list(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Yangi message yaratish")
    def create(self, request, *args, **kwargs):
        return super(MessageViews, self).create(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali messageni o'chirish")
    def destroy(self, request, *args, **kwargs):
        """
        Id orqali messageni o'chirish
        """
        return super(MessageViews, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali messageni yangilash")
    def update(self, request, *args, **kwargs):
        """
        Id orqali messageni yangilash
        """
        return super(MessageViews, self).update(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali messageni qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        """
        Id orqali messageni qisman yangilash
        """
        return super(MessageViews, self).partial_update(self, request, *args, **kwargs)


class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers
