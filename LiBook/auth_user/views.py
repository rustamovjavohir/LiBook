from datetime import datetime, timedelta

import jwt
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action, permission_classes
from drf_yasg.utils import swagger_auto_schema

# from ..app.models import User
from app.models import User
from .serializers import LoginSerializer
from app.serializers import UserSerializers
from rest_framework.viewsets import ModelViewSet

from .user_jwt import L_JWTAuthentication
from .utils import my_books, admin, check_token
from app.utils import same_books


class RegisterViews(GenericAPIView):
    serializer_class = UserSerializers
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Ro'yhatdan o'tish")
    def post(self, request):
        """
        Foydalanuvchini registratsiay qilish
        """
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginViews(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Login")
    def post(self, request):
        """
        Foydalanuvchini tizimga kirishi (login)
        """
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            "id": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=60),
            "iat": datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.data = {
            "token": token
        }
        response.set_cookie(key='Token', value=token, httponly=True)
        return response


class UserViews(GenericAPIView):

    authentication_classes = [L_JWTAuthentication]
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializers
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(operation_summary="Foydalanuvchi haqidagi malumotlar")
    def get(self, request):
        """
        Foydalanuvchi haqidagi ma'lumotlarni namoish etadi, olgan kitoblari
        """
        payload = check_token(request)
        user = User.objects.filter(id=payload.get('id')).first()
        serializer = UserSerializers(user)
        data = serializer.data
        data['my_books'] = my_books(u_id=user.id)
        data['same_books'] = same_books(user_id=user.id)
        if self.request.user.is_staff:
            data['users'] = admin(user)
        return Response(data)

    @swagger_auto_schema(operation_summary="Foydalanuvchi ma`lumotlarini yangilash")
    def put(self, request, *args, **kwargs):
        """
        Foydalanuvchi ma`lumotlarini yangilash
        """
        user = request.user
        data = request.data
        serializer = UserSerializers(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutViews(APIView):

    @swagger_auto_schema(operation_summary="Tizimdan chiqish")
    def post(self, request):
        """
        Logout qiladigan funksiya
        """
        response = Response()
        response.delete_cookie('Token')
        response.data = {
            "massage": "Tizimdam muvoffaqiyatni tark endinggiz"
        }
        return response


