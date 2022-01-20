from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class UserViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)

# class AkkountViews(ModelViewSet):
#     queryset = Akkount.objects.all()
#     serializer_class = AkkountSerializers

class BookViews(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data=[]
        book_ = Book.objects.get(id=int(id))
        book_data = {
            "id": book_.id,
            "author": book_.author,
            "name": book_.name,
            "about": book_.about,
            "file": book_.file_url,
            "add_date": book_.add_date.strftime("%Y-%m-%d %H:%M:%S"),
            "photo": book_.photo_url,
            "status": book_.status,
            "type": book_.type,
            "lang": book_.lang,
            "views": book_.views,
            "category": book_.category.id
        }
        comment = Message.objects.filter(book=int(id))
        for i in comment:
            reply_message = []
            a = ReplyMessage.objects.filter(basic_message=i)
            for j in a:
                reply_message.append({
                    'id':j.id,
                    'username':j.user.user.username,
                    'message':j.message,
                    'date':j.date.strftime("%Y-%m-%d %H:%M:%S")
                })
            d = {
                'id':i.id,
                'username':i.user.user.username,
                'message':i.message,
                'date':i.date.strftime("%Y-%m-%d %H:%M:%S"),
                'views':i.views,
                'reply_message':reply_message
            }
            data.append(d)

        return Response({"book":book_data,
                         'message':data})

class BoxViews(ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializers
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        data=[]
        for item in Box.objects.all():
            if item.user.id == int(id):
                d = {
                    'id':item.id,
                    'book_name':item.book.name,
                    'book_photo':item.book.photo_url,
                    'book_author':item.book.author,
                    'book_category':item.book.category.name,
                    'user':item.user.id,
                    'date':item.date.strftime("%Y-%m-%d %H:%M:%S"),
                }
                data.append(d)
        return Response({"result":data})


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

#commit
