from datetime import datetime, timedelta

import jwt
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

# from ..app.models import User
from app.models import User
from app.serializers import UserSerializers
from .user_jwt import L_JWTAuthentication
from .utils import my_books


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
        token = request.COOKIES.get('Token')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload.get('id')).first()
        serializer = UserSerializers(user)
        data = serializer.data
        data['my_books'] = my_books(u_id=user.id)
        return Response(data)


class LogoutViews(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('Token')
        response.data = {
            "massage": "success"
        }
        return response
#this is comment