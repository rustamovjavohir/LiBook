from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .utils import BookPagination, UserPagination
from auth_user.user_jwt import L_JWTAuthentication


class UsersViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = [L_JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    pagination_class = UserPagination

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(data={'detail': 'You do not have permission to perform this action / '
                                            'Only admins have permission'})
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = UserSerializers(user)
        return Response(serializer.data)


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



