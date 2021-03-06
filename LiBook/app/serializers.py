from rest_framework.serializers import ModelSerializer

from .models import *


class UserSerializers(ModelSerializer):

    class Meta:
        model = User
        fields = (
        'id', 'username', 'first_name', 'last_name', "email", 'date_of_birth', 'address', 'password')  # 'password'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # if self.context['request'].user.is_staff:
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class CategorySerializers(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializers(ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BoxSerializers(ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"
        extra_kwargs = {
            'is_delivered': {'write_only': True},
        }


class AdviceSerializers(ModelSerializer):
    class Meta:
        model = Advice
        fields = "__all__"