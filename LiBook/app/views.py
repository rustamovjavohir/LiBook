from datetime import timedelta

import jwt as jwt
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .utils import BookPagination, UserPagination


class UsersViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)
    pagination_class = UserPagination

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = UserSerializers(user)
        return Response(serializer.data)


# class AkkountViews(ModelViewSet):
#     queryset = Akkount.objects.all()
#     serializer_class = AkkountSerializers


class BookViews(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    pagination_class = BookPagination

    @csrf_exempt
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = []
        book_ = get_object_or_404(klass=Book, id=int(id))
        book_data = {
            "id": book_.id,
            "author": book_.author,
            "name": book_.name,
            "about": book_.about,
            "file": book_.file_url,
            "add_date": book_.add_date.strftime("%Y-%m-%d, %H:%M:%S"),
            "photo": book_.photo_url,
            "status": book_.status,
            "type": book_.type,
            "lang": book_.lang,
            "views": book_.views,
            "category": book_.category.id
        }
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
                data.append(d)

        return Response({"book": book_data,
                         'message': data})


class BoxViews(ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializers

    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data = []
        for item in Box.objects.all():
            if item.user.id == int(id):
                d = {
                    'id': item.id,
                    'book_name': item.book.name,
                    'book_photo': item.book.photo_url,
                    'book_author': item.book.author,
                    'book_category': item.book.category.name,
                    'user': item.user.id,
                    'date': item.date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                data.append(d)
        return Response({"result": data})


class CateogryViews(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class MessageViews(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers


class ReplyMessageViews(ModelViewSet):
    queryset = ReplyMessage.objects.all()
    serializer_class = ReplyMessageSerializers


class AdviceViews(ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializers


class RegisterViews(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginViews(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.data = {
            "token": token
        }
        response.set_cookie(key='token', value=token, httponly=True)
        return response


class UserViews(APIView):

    def get(self, request):
        token = request.COOKIES.get('token')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload.get('id')).first()
        serializer = UserSerializers(user)
        return Response(serializer.data)


class LogoutViews(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            "massage": "success"
        }
        return response

