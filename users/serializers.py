from rest_framework import serializers
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(max_length=20, required=False)
    email = serializers.EmailField(max_length=100, required=True)
    telegram_id = serializers.CharField(max_length=50, required=True)
    username = serializers.CharField(max_length=50, required=False)
    first_name = serializers.CharField(max_length=50, required=False)
    last_name = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('user_phone', 'email', 'telegram_id', 'username', 'first_name', 'last_name', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_telegram_id(self, value):
        if User.objects.filter(telegram_id=value).exists():
            raise serializers.ValidationError("This Telegram ID is already registered.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user