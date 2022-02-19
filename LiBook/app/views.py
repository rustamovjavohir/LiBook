from datetime import timedelta

import jwt as jwt
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, TokenAuthentication,BaseAuthentication, BasicAuthentication,RemoteUserAuthentication
# from rest_framework_simplejwt import authentication
from .serializers import *
from .utils import BookPagination, UserPagination
from auth_user.user_jwt import L_JWTAuthentication

from massages.models import Message, ReplyMessage

from auth_user.utils import my_books


class UsersViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # permission_classes = [IsAdminUser]
    # authentication_classes = [L_JWTAuthentication]
    pagination_class = UserPagination

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = UserSerializers(user)
        return Response(serializer.data)


class BookViews(ModelViewSet):
    search_fields = ['author', 'name']
    filter_backends = (filters.SearchFilter,)
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    pagination_class = BookPagination
    # authentication_classes = [L_JWTAuthentication, ]
    # permission_classes = [IsAdminUser, ]

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = BookSerializers(book)
        id = kwargs['pk']
        message_data = []
        if Message.objects.filter(book=int(id)) is not None:
            comment = Message.objects.filter(book=int(id))
            for i in comment:
                reply_message = []
                a = ReplyMessage.objects.filter(basic_message=i)
                for j in a:
                    reply_message.append({
                        'id': j.id,
                        'username': j.user.username,
                        'message': j.message,
                        'date': j.date.strftime("%Y-%m-%d %H:%M:%S")
                    })
                d = {
                    'id': i.id,
                    'username': i.user.username,
                    'message': i.message,
                    'date': i.date.strftime("%Y-%m-%d %H:%M:%S"),
                    'views': i.views,
                    'reply_message': reply_message
                }
                message_data.append(d)
        r_data = serializer.data
        r_data["message"] = message_data
        return Response(data=r_data)


class BoxViews(ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializers
    # authentication_classes = [L_JWTAuthentication]
    # permission_classes = [IsAdminUser]

    @action(methods=['post'], detail=False, url_path='user_books', url_name='user_books')
    def box(self, request, pk=None, *args, **kwargs):
        # u_id = int(request.user.id)
        u_id = request.data.get("u_id")
        user_books_data = my_books(u_id=u_id)
        return Response(user_books_data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Box.objects.all()
        box = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = BoxSerializers(box)
        return Response(serializer.data)


class CateogryViews(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class AdviceViews(ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializers








