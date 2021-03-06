from auth_user.user_jwt import L_JWTAuthentication
from auth_user.utils import check_token
from auth_user.utils import my_books
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from massages.models import Message, ReplyMessage
from rest_framework import filters, status
from rest_framework.decorators import action, permission_classes as view_permission_classes
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .utils import BookPagination, UserPagination, discount, countless, sed_exel


class UsersViews(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAdminUser]
    authentication_classes = [L_JWTAuthentication]
    pagination_class = UserPagination

    @swagger_auto_schema(operation_summary="Foydalanuvchilar ma`lumotlarini chop etish")
    def list(self, request, *args, **kwargs):
        return super(UsersViews, self).list(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Admin tomonidan foydalanuvchi qo'shish")
    def create(self, request, *args, **kwargs):
        return super(UsersViews, self).create(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Admin tomonidan foydalanuvchi ma'lumotlarini yangilash")
    def update(self, request, *args, **kwargs):
        super(UsersViews, self).update(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Admin tomonidan foydalanuvchi ma'lumotlarini qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        super(UsersViews, self).partial_update(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali foydalanuvchini o'chirib tashlash")
    def destroy(self, request, *args, **kwargs):
        return super(UsersViews, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali foydalanuvchi ma`lumotlarini chop etish")
    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = UserSerializers(user)
        return Response(serializer.data)


class BookViews(ModelViewSet):
    search_fields = ['author', 'name', 'category']
    filter_backends = (filters.SearchFilter,)
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    pagination_class = BookPagination
    authentication_classes = [L_JWTAuthentication, ]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Kitoblar ro'yhatini chop etish")
    @view_permission_classes((AllowAny,))
    def list(self, request, *args, **kwargs):
        """
        Kitoblar ro'yhatini chop etish
        """
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = self.filter_queryset(self.get_queryset())
        queryset = discount(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Yangi kitob yaratish (qo'shish)")
    def create(self, request, *args, **kwargs):
        """
        Ushbu buyruqni faqat admin huquqiga ega bo'lganlar bera oladi
        """
        self.authentication_classes = [L_JWTAuthentication]
        return super(BookViews, self).create(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Kitobni o'chirish")
    def destroy(self, request, *args, **kwargs):
        """
        Ushbu buyruqni faqat admin huquqiga ega bo'lganlar bera oladi
        """
        self.authentication_classes = [L_JWTAuthentication]
        return super(BookViews, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Kitob haqidagi malumotlarni yangilash")
    def update(self, request, *args, **kwargs):
        self.authentication_classes = [L_JWTAuthentication]
        return super(BookViews, self).update(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Kitob haqidagi ma'lumotlarni qisman yangilash")
    def partial_update(self, request, *args, **kwargs):
        self.authentication_classes = [L_JWTAuthentication]
        return super(BookViews, self).partial_update(self, request, *args, **kwargs)

    @csrf_exempt
    @swagger_auto_schema(operation_summary="Id orqali kitob haqidagi ma'lumotlarni chop etish")
    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated]
        self.authentication_classes = [L_JWTAuthentication]
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


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ('author', 'name', 'category')
    permission_classes = [AllowAny]
    pagination_class = BookPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = discount(queryset)
        sed_exel()  # Adminga har hafta shanba kuni email jo'natiladi
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(countless(serializer.data))

        serializer = self.get_serializer(queryset, many=True)
        return Response(countless(serializer.data))

    @swagger_auto_schema(operation_summary="Kitoblar ro'yhatini chop etish")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookRetrieve(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Id orqali kitob haqidagi malumotlarni chop etish")
    def get(self, request, *args, **kwargs):
        """
       Id orqali kitobni chop etish
        """
        return super().get(request, *args, **kwargs)


class BoxViews(ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializers
    # authentication_classes = [L_JWTAuthentication]
    # permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Foydalanuvchining barcha kitoblarini chop etish")
    @action(methods=['post'], detail=False, url_path='user_books', url_name='user_books')
    def box(self, request, *args, **kwargs):
        self.serializer_class = None
        """
         Ushbu buyruqni faqat admin amalga oshiroladi.    
        """
        u_id = request.data.get("u_id")
        user_books_data = my_books(u_id=u_id)
        return Response(user_books_data)

    @swagger_auto_schema(operation_summary="Id orqali boxlar haqidagi ma'lumotlarni chop etish")
    def retrieve(self, request, *args, **kwargs):
        """
         Ushbu buyruqni faqat admin amalga oshiroladi
        """
        queryset = Box.objects.all()
        box = get_object_or_404(queryset, pk=kwargs['pk'])
        serializer = BoxSerializers(box)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="Mavjud boxlarni ro'yhatini chop etadi")
    def list(self, request, *args, **kwargs):
        """
        Ushbu buyruqni faqat admin amalga oshiroladi (list)
        """
        return super(BoxViews, self).list(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Id orqali boxni o'chirib tashlash")
    def destroy(self, request, *args, **kwargs):
        """
        Ushbu buyruqni faqat admin amalga oshiroladi (delete)
        """
        return super(BoxViews, self).destroy(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Box haqidagi ma'lumotlarni yangilash ")
    def update(self, request, *args, **kwargs):
        """
         Ushbu buyruqni faqat admin amalga oshiroladi (update)
        """
        return super(BoxViews, self).update(self, request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Box haqidagi ma'lumotlarni qisman yangilaydi")
    def partial_update(self, request, *args, **kwargs):
        """
         Ushbu buyruqni faqat admin amalga oshiroladi (partial update)
        """
        return super(BoxViews, self).partial_update(self, request, *args, **kwargs)


class BoxCreate(GenericAPIView):
    serializer_class = BoxSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [L_JWTAuthentication]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Foydalanuvchi va kitobni bog'lovchi buyruq")
    def post(self, request, *args, **kwargs):
        """
           Kitobni savatchaga qo'shish
        """
        payload = check_token(request)
        box = Box(book_id=request.data.get('book'), user_id=payload.get('id'), date=datetime.now())
        box.save()
        return Response({"message": "success"})


class Basket(GenericAPIView):
    serializer_class = BoxSerializers
    permission_classes = [IsAuthenticated]
    authentication_classes = [L_JWTAuthentication]

    @swagger_auto_schema(operation_summary="Savatchadagi kitoblar royhatini ko'rish")
    def get(self, request, **kwargs):
        boxs = Box.objects.filter(user_id=request.user.id, is_delivered=False, is_paid=False)
        box_ser = BoxSerializers(boxs, many=True)
        return Response(box_ser.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Savatchadi kitoblarni sotib "
                                           "olish (Bir nechtasini bir vaqtda olsa ham bo'ladi)")
    def post(self, request, *args, **kwargs):
        box_objects = []
        box_id_list = str(request.data.get('data')).replace(',', ' ').split(' ')
        for item in box_id_list:
            try:
                boxs = Box.objects.filter(id=int(item), is_delivered=False, is_paid=False).first()
                boxs.is_paid = True
                boxs.save()
                box_objects.append(boxs)
            except Exception as ex:
                print(ex)
        serializer = BoxSerializers(box_objects, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "books not found"}, status=status.HTTP_200_OK)


class Delivery(GenericAPIView):
    serializer_class = BoxSerializers
    queryset = Box.objects.filter(is_delivered=False, is_paid=True)
    permission_classes = [IsAdminUser]
    authentication_classes = [L_JWTAuthentication]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user',)

    @swagger_auto_schema(operation_summary="Yetkazib berilishi kerak bolgan kitoblar")
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="Kitoblarni yetkazib berilganini tasdiqlash")
    def post(self, request, *args, **kwargs):
        box_objects = []
        box_id_list = str(request.data.get('data')).replace(',', ' ').split(' ')
        for item in box_id_list:
            try:
                boxs = Box.objects.filter(id=int(item), is_delivered=False, is_paid=True).first()
                boxs.is_delivered = True
                boxs.save()
                box_objects.append(boxs)
            except Exception as ex:
                print(ex)
        serializer = BoxSerializers(box_objects, many=True)
        if serializer.data:
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "books not found"}, status=status.HTTP_200_OK)


class CateogryViews(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminUser]
    authentication_classes = L_JWTAuthentication


class AdviceViews(ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializers








