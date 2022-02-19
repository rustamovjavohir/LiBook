from datetime import datetime, timedelta

import jwt
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action, permission_classes

# from ..app.models import User
from app.models import User
from app.serializers import UserSerializers
from rest_framework.viewsets import ModelViewSet

from .user_jwt import L_JWTAuthentication
from .utils import my_books, admin, check_token


class RegisterViews(APIView):
    def post(self, request):
        serializer = UserSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginViews(APIView):
    permission_classes = [AllowAny, ]

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


class UserViews(APIView):

    authentication_classes = [L_JWTAuthentication]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        payload = check_token(request)
        user = User.objects.filter(id=payload.get('id')).first()
        serializer = UserSerializers(user)
        data = serializer.data
        data['my_books'] = my_books(u_id=user.id)
        data['users'] = admin(user)
        return Response(data)

    def put(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        serializer = UserSerializers(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutViews(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('Token')
        response.data = {
            "massage": "success"
        }
        return response
