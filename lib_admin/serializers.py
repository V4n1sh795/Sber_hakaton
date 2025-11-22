from rest_framework import serializers
from books.models import Book
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и управления пользователями через API"""
    full_name = serializers.ReadOnlyField()
    role_display = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'name', 'lastname', 'patronymic', 
            'phone', 'full_name', 'role_display', 
            'is_staff', 'is_active', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'email': {'required': True},
            'name': {'required': True},
            'lastname': {'required': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            username=validated_data['email'],
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance
