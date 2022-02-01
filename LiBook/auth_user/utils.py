from app.models import Box, Book
from app.serializers import BoxSerializers, BookSerializers


def my_books(u_id, *args, **kwargs):
    box = Box.objects.filter(user=u_id)
    box_ser = BoxSerializers(box, many=True)
    for item in box_ser.data:
        book = Book.objects.filter(id=item['book']).first()
        book_ser = BookSerializers(book, many=False)
        item['book'] = book_ser.data
    return box_ser.data
