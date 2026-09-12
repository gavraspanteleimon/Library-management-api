from enum import member

from rest_framework import serializers
from .models import Author, Book, Member, Loan, Category
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'bio', 'birth_date']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'categories']

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['user', 'phone', 'address']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['book', 'member', 'loan_date', 'return_date', 'is_returned']


class MemberRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField()
    address = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(username=username, password=password)
        member = Member.objects.create(user=user, **validated_data)
        return member

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.user.username,  # ρητά: πήγαινε ΜΕΣΑ στη σχέση
            'phone': instance.phone,
            'address': instance.address,
        }