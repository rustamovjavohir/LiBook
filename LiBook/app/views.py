from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import *

class UserViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

class AkkountViews(ModelViewSet):
    queryset = Akkount.objects.all()
    serializer_class = AkkountSerializers

class BookViews(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

class BoxViews(ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializers

class MessageViews(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers

class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers
