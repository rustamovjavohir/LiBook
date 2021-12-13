from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializers(ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
