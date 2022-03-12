import jwt
from app.models import Box, Book, Discount
from app.serializers import BoxSerializers, BookSerializers

from app.models import User
from app.serializers import UserSerializers
from rest_framework.exceptions import AuthenticationFailed

from app.utils import discount


def my_books(u_id, *args, **kwargs):
    box = Box.objects.filter(user=u_id)
    box_ser = BoxSerializers(box, many=True)
    for item in box_ser.data:
        book = Book.objects.filter(id=item['book']).first()
        book_ser = BookSerializers(book, many=False)
        book_ser_data = book_ser.data
        del book_ser_data['count']
        dic_book = Discount.objects.filter(book_id=book.id, is_deleted=False).first()
        if dic_book:
            book_ser_data['price'] = dic_book.new_price
        item['book'] = book_ser_data
    return box_ser.data


def admin(user):
    if user.is_staff:
        users = User.objects.all()
        users_ser = UserSerializers(users, many=True)
        return users_ser.data
    return None


def check_token(request):
    token = request.COOKIES.get('Token')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
