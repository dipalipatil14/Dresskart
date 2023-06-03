from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Note, UserImage, CustomUser

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class ImageSerializer(ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'

# class CustomUserSerializer(ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password', 'is_verified']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_verified']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


