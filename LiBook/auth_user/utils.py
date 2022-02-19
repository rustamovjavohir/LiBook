import jwt
from app.models import Box, Book
from app.serializers import BoxSerializers, BookSerializers

from app.models import User
from app.serializers import UserSerializers
from rest_framework.exceptions import AuthenticationFailed


def my_books(u_id, *args, **kwargs):
    box = Box.objects.filter(user=u_id)
    box_ser = BoxSerializers(box, many=True)
    for item in box_ser.data:
        user = User.objects.filter(id=u_id).first()
        book = Book.objects.filter(id=item['book']).first()
        book_ser = BookSerializers(book, many=False)
        item['username'] = user.username
        item['book'] = book_ser.data
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
