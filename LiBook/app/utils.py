import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

import pytz
import xlsxwriter as xlsxwriter
from openpyxl import Workbook
from rest_framework.pagination import PageNumberPagination

from .models import Book, Discount, Box
from .serializers import BookSerializers

EMAIL_ADDRESS = "rustamovj399@gmail.com"
EMAIL_PASSWORD = "wgmemwvlfxflrdts"


class BookPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UserPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000


def discount(queryset):
    books = queryset
    dic_books = Discount.objects.filter(is_deleted=False)
    for dic_book in dic_books:
        for book in books:
            if dic_book.book_id == book.id:
                book.price = dic_book.new_price
    return books


def countless(serializer_data):
    for book in serializer_data:
        del book['count']
    return serializer_data


def book_category():
    from .models import Category
    category_list = Category.objects.all()
    CATEGORY_NAME = ()
    for obj in category_list:
        my_tuple = ((f"{obj.name.upper()}", f"{obj.name}"),)
        CATEGORY_NAME += my_tuple
    return CATEGORY_NAME


def same_books(user_id):
    if Box.objects.filter(user_id=user_id):
        last_book = Box.objects.filter(user_id=user_id).last().book
        books = Book.objects.filter(category__icontains=last_book.category, author__icontains=last_book.author)
        books_ser = BookSerializers(books, many=True)
        return books_ser.data
    return []


def sed_exel():
    x = datetime.now()
    if x.strftime("%A") == 'Saturday':
        message = EmailMessage()
        message['Subject'] = "Haftalik ma`lumot"
        message['From'] = EMAIL_ADDRESS
        message['To'] = 'rustamovj366@gmail.com'
        message.set_content('File attached')
        file = '2022-03-12.xlsx'
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(message)


def write_to_exel():
    boxs = Box.objects.filter(is_delivered=True, is_paid=True)
    filename = f'{datetime.date(datetime.now())}.xlsx'
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet()
    utc = pytz.UTC
    create_xl_file()
    for row, box in enumerate(boxs):
        box_date = box.date.replace(tzinfo=utc)
        start_date = (datetime.now() - timedelta(days=7)).replace(tzinfo=utc)
        now = datetime.now().replace(tzinfo=utc)
        if start_date <= box_date <= now:
            ws.write(row, 0, box.user.username)
            ws.write(row, 1, box.book.name)
            ws.write(row, 2, str(box.date))
    wb.close()
    return filename


def create_xl_file() -> None:
    date = datetime.date(datetime.now())

    if not os.path.isfile(os.path.join(f'{date}.xlsx')):
        wb = Workbook()
        ws = wb.active
        ws.title = f"{date}.xlsx"
        ws.append(('user', 'book', 'date'))
        wb.save(f"{date}.xlsx")
