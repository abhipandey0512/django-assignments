from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import books

# books
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = books
        fields = ('title', 'author', 'description', 'published_date', 'price', 'created_at', 'updated_at')
        
# signup

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = books 
        fields = '__all__'  

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


#login
class Loginserializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

